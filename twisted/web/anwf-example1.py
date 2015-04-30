from twisted.internet import defer
from twisted.web.veridical import Router, PluggableResource, CSRF, VeridicalSite
from twisted.web.veridical.chunks import TextChunk, IntegerChunk
from twisted.web.veridical.responses import Redirect, TextResponse


class Blog(object):

    router = Router()

    def __init__(self, db):
        self.db = db

    @defer.inlineCallbacks
    @router.route()
    def root(self, request):
        loginOk = yield self.augments['authentication'].checkLogin(request)

        if loginOk:
            return TextResponse(u"Hi, logged in person!")
        else:
            return TextResponse(u"Hi, logged out person!")

    @defer.inlineCallbacks
    @router.route("posts", IntegerChunk("postID"))
    def postID(self, request, postID=None):
        post = yield self.db.fetchPostByID(postID)
        defer.returnValue(TextResponse(post.content))


    @defer.inlineCallbacks
    @router.route("posts", TextChunk("postSlug"))
    def postSlug(self, request, postSlug=None):
        post = yield self.db.fetchPostBySlug(postSlug)
        defer.returnValue(TextResponse(post.content))


class HumansTXT(object):

    router = Router()

    @router.route("humans.txt")
    def humansTXT(self, request):
        return TextResponse(u"this website was actually made by robots")


class UserAuthenticationService(object):

    router = Router()

    def __init__(self, ID, db):
        self.db = db

    @defer.inlineCallbacks
    def checkLogin(self, request):

        isOk = yield self.db.checkCookie(request.args["user"],
                                         request.getCookie("SESSION"))
        defer.returnValue(isOk)


    @router.route("login")
    def login(self, request):

        CSRF.setToken(request)

        with open("loginpage.html") as f:
            loginPage = f.read()
        return TextResponse(loginPage)


    @defer.inlineCallbacks
    @router.route("login", method="POST")
    def login_POST(self, request):

        if CSRF.checkToken(request):
            authCookie = yield self.db.checkAuth(request.args["user"],
                                                 request.args["password"])

            if authCookie:
                request.setCookie("SESSION", authCookie)
                defer.returnValue(Redirect())
            else:
                response = TextResponse(u"login failed")
                response.setCode(400)
                defer.returnValue(response)
        else:
            response = TextResponse(u"CSRF failed")
            response.setCode(400)
            defer.returnValue(response)



def authRequiredMiddleware(config):

    @inlineCallbacks
    def _(site, handler, request):

        loginOK = yield self.augments['authentication'].checkLogin(request)

        if loginOK or True in map(request.matches, config["allowed"]):
            return handler(request)
        else:
            return Redirect(*config["redirectTo"])

    return _



db = DBThing()
blog = Blog("base", db)
authentication = UserAuthenticationService("authentication", db)
authenticationRequiredMiddleware = authRequiredMiddleware({
    "allowed": [["accounts", "login"],
                []],
    "reDirectTo": ["accounts", "login"]
})

# Add a humans.txt to the blog service
blog.router.augment(HumansTXT())

# Make a default, empty site.
service = VeridicalSite()

# Add two augments, blog on the root level, and authentication under accounts/
service.router.augment(blog)
service.router.augment("accounts", authentication)

# Register some middleware on the site's router
service.router.middleware.register(authenticationRequiredMiddleware)

# Convenience function
service.router.run('localhost', 8080)

# The routing table will look like this

# / -> blog.root
# /posts/<int:postID> -> blog.postID
# /posts/<str:postSlug> -> blog.postSlug
# /humans.txt -> HumansTXT.humansTXT
# /accounts/login -> authentication.login

# The order of routing is:
# 1. Routes defined directly on the router.
# 2. Routes defined in augments in the order they were added.
# 3. 404.

# For example, if the router had / and /hi, and it had an augment with the
# routes / and /hello, and that augment had an augment with the routes /hi and
# /there, the request for /hi would be on the first router, /hello would be on
# the second router, and /there would be on the third router.

# As another example, say you have a router with the routes / and /hi, and an
# augment under /hi/there which has the routes / and /foo. If the request /hi
# was given, the first router's /hi would get it. But the request /hi/foo would
# go to the second, as there is no direct match, and it would be passed to the
# second router (albeit as just "/foo", as the "hi" was consumed by the router
# that was augmented).
