import os
import webapp2
import jinja2
from google.appengine.ext import db
import urllib2
import re

template_dir = os.path.join(os.path.dirname(__file__), 'templates')
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir), autoescape=True)

class Handler(webapp2.RequestHandler):
    def write(self, *a, **kw):
        self.response.out.write(*a, **kw)
    def render_str(self, template, **params):
        t = jinja_env.get_template(template)
        return t.render(params)
    def render(self, template, **kw):
        self.write(self.render_str(template, **kw))
        
class MainPage(Handler):
    def get(self):
        self.render("formrss.html")
    def post(self):
        x = self.request.get("rssquery")
        url = "http://www.quora.com/" + x + "/rss"
        content = urllib2.urlopen(url).read()
        content = content.decode('utf-8')
        allTitles =  re.compile('<title>(.*?)</title>')
        allLinks = re.compile('<link>(.*?)</link>')
        list = re.findall(allTitles,content)
        linklist = re.findall(allLinks,content)
        self.render("frontrss.html", list = list, linklist = linklist)
        


app = webapp2.WSGIApplication([('/', MainPage)], debug=True)