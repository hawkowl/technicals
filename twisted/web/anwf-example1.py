from twisted.internet import defer
from twisted.web.veridical import Router, PluggableResource, CSRF, VeridicalSite
from twisted.web.veridical.chunks import TextChunk, IntegerChunk
from twisted.web.veridical.responses import Redirect, TextResponse


class Blog(PluggableResource):

    app = Router()

    def __init__(self, db):
        self.db = db

    @defer.inlineCallbacks
    @app.route()
    def root(self, request):
        loginOk = yield self.augments['authentication'].checkLogin(request)

        if loginOk:
            return TextResponse(u"Hi, logged in person!")
        else:
            return TextResponse(u"Hi, logged out person!")

    @defer.inlineCallbacks
    @app.route("posts", IntegerChunk("postID"))
    def postID(self, request, postID=None):
        post = yield self.db.fetchPostByID(postID)
        defer.returnValue(TextResponse(post.content))


    @defer.inlineCallbacks
    @app.route("posts", TextChunk("postSlug"))
    def postSlug(self, request, postSlug=None):
        post = yield self.db.fetchPostBySlug(postSlug)
        defer.returnValue(TextResponse(post.content))



class UserAuthenticationService(PluggableResource):

    app = Router()

    def __init__(self, ID, db):
        self.db = db

    @defer.inlineCallbacks
    def checkLogin(self, request):

        isOk = yield self.db.checkCookie(request.args["user"],
                                         request.getCookie("SESSION"))
        defer.returnValue(isOk)


    @app.router("login")
    def login(self, request):

        CSRF.setToken(request)

        with open("loginpage.html") as f:
            loginPage = f.read()
        return loginPage


    @defer.inlineCallbacks
    @app.router("login", method="POST")
    def login_POST(self, request):

        if CSRF.checkToken(request):
            authCookie = yield self.db.checkAuth(request.args["user"],
                                                 request.args["password"])

            if authCookie:
                request.setCookie("SESSION", authCookie)
            else:
                raise Exception("Login Failed") # lol?
        else:
            raise CSRF.failed()



def authRequiredTween(config):

    @inlineCallbacks
    def _(site, handler, request):

        loginOK = yield self.augments['authentication'].checkLogin(request)

        if loginOK or True in map(request.matches, config["allowed"]):
            return handler(request)
        else:
            return Redirect(config["redirectTo"])

    return _



db = DBThing()

service = VeridicalSite()
service.augment(MySweetWebService("base", db))
service.augment("accounts",
                UserAuthenticationService("authentication", db))
service.tweens.register(authRequiredTween({
    "allowed": [["accounts", "login"],
                []],
    "reDirectTo": ["accounts", "login"]
}))
service.run('localhost', 8080)
