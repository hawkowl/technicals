from twisted.internet import defer
from twisted.web.veridical import Router, PluggableResource, CSRF
from twisted.web.veridical.chunks import TextChunk, IntegerChunk


class MySweetWebService(PluggableResource):

    app = Router()

    def __init__(self, db):
        self.db = db

    @defer.inlineCallbacks
    @app.route("posts", IntegerChunk("postID"))
    def postID(self, request, postID=None):

        post = yield self.db.fetchPostByID(postID)
        defer.returnValue(post.content)


    @defer.inlineCallbacks
    @app.route("posts", TextChunk("postSlug"))
    def postSlug(self, request, postSlug=None):
        """
        Only available to logged in users.
        """
        loginOk = yield self.augments['authentication'].checkLogin(request)

        if loginOk:
            post = yield self.db.fetchPostBySlug(postSlug)
            defer.returnValue(post.content)



class UserAuthenticationService(object):

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



db = DBThing()

service = MySweetWebService("base", db)
service.augment("authentication",
                UserAuthenticationService("authentication", db))
service.run('localhost', 8080)
