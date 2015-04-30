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

service = VeridicalSite()

service.augment(blog)
service.augment("accounts", authentication)

service.middleware.register(authenticationRequiredMiddleware)

service.run('localhost', 8080)
