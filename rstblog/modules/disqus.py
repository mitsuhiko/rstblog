# -*- coding: utf-8 -*-
"""
    rstblog.modules.disqus
    ~~~~~~~~~~~~~~~~~~~~~~

    Implements disqus element if asked for.
    
    To use this, include disqus in the list of modules in your ``config.yml`` file,
    and add a configuration variable to match your settings : ``disqus.shortname`` 
    
    To prevent comments on a particular page, set ``disqus = no`` in the page's YAML preamble.

    :copyright: (c) 2012 by Martin Andrews.
    :license: BSD, see LICENSE for more details.
"""
from jinja2 import contextfunction

@contextfunction
def get_disqus(context):
    disqus_txt="""
<div id="disqus_thread"></div>
<script type="text/javascript">
    var disqus_shortname = '%s'; // required: replace example with your forum shortname

    /* * * DON'T EDIT BELOW THIS LINE * * */
    (function() {
        var dsq = document.createElement('script'); dsq.type = 'text/javascript'; dsq.async = true;
        dsq.src = 'http://' + disqus_shortname + '.disqus.com/embed.js';
        (document.getElementsByTagName('head')[0] || document.getElementsByTagName('body')[0]).appendChild(dsq);
    })();
</script>
<noscript>Please enable JavaScript to view the <a href="http://disqus.com/?ref_noscript">comments powered by Disqus.</a></noscript>
<a href="http://disqus.com" class="dsq-brlink">blog comments powered by <span class="logo-disqus">Disqus</span></a>
""" % (
 context['builder'].config.root_get('modules.disqus.shortname', 'YOUR-DISQUS-SHORTNAME'),
)

    if not context['config'].get('disqus', True):
        disqus_txt='' # "<h1>DISQUS DEFEATED</h1>"
        
    return disqus_txt.encode('utf-8')


def setup(builder):
    builder.jinja_env.globals['get_disqus'] = get_disqus
