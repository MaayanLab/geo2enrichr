App.Model.Share = Backbone.Model.extend({
    defaults: [
        {
            link: 'http://twitter.com/share',
            image: 'web/site/image/share/twitter.png'
        },
        {
            link: 'http://www.facebook.com/sharer/sharer.php?u=http://amp.pharm.mssm.edu/g2e/',
            image: 'web/site/image/share/facebook.png'
        },
        {
            link: 'https://plus.google.com/share?url=http://www.maayanlab.net/harmoziome',
            image: 'web/site/image/share/google-plus.png'
        },
        {
            link: 'https://www.linkedin.com/shareArticle?url=http://amp.pharm.mssm.edu/g2e/',
            image: 'web/site/image/share/linkedin.png'
        }
    ]
});
