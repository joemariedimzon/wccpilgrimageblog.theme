from five import grok
from Products.CMFCore.utils import getToolByName
from Products.CMFCore.interfaces import ISiteRoot
from plone.app.discussion.interfaces import IConversation, IComment

grok.templatedir('templates')

class authors_view(grok.View):
    grok.context(ISiteRoot)
    grok.require('zope2.View')
    
    @property
    def catalog(self):
        return getToolByName(self.context, 'portal_catalog')
    
    @property
    def membership(self):
        return getToolByName(self.context, 'portal_membership')
    
    def author_data(self):
        membership = self.membership
        request = self.request
        if request.form:
            if 'id' in request.form:
                author = membership.getMemberById(request.form['id'])
                if author:
                    return True
        return False
    
    def author_info(self):
        membership = self.membership
        request = self.request
        results = {'fullname':'', 'portrait':'', 'user_biography':'', 'id':'', 'location':'', 'language':'', 'twitter':''}
        if request.form:
            if 'id' in request.form:
                author = membership.getMemberById(request.form['id'])
                if author:
                    results['fullname'] = author.getProperty('fullname')
                    results['portrait'] = membership.getPersonalPortrait(request.form['id'])
                    results['user_biography'] = author.getProperty('user_biography')
                    results['id'] = request.form['id']
                    results['location'] = author.getProperty('location')
                    results['language'] = author.getProperty('language')
                    results['twitter'] = author.getProperty('twitter_username')
        return results
                
    def posts(self, author=None):
        catalog = self.catalog
        brains = catalog.unrestrictedSearchResults(dict(sort_on='created', sort_order='reverse', portal_type='News Item', review_state='published'))
        results = []
        for brain in brains:
            if author in brain.listCreators:
                obj = brain._unrestrictedGetObject()
                data = {}
                data['creator'] = brain.listCreators
                data['modified'] = brain.modified
                data['title'] = brain.Title
                data['description'] = brain.description
                data['path'] = brain.getPath()
                data['obj'] = obj
                results.append(data)
                if len(results) ==4:
                    break;
        return results
    
    def totalComments(self, context=None):
        comments = IConversation(context)
        return len(comments)
        
        
                
