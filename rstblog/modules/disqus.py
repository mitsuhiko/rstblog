# -*- coding: utf-8 -*-
"""
    rstblog.modules.disqus
    ~~~~~~~~~~~~~~~~~~~~~~

    Implements disqus element if asked for.
    
    To use this, include ``disqus`` in the list of modules in your ``config.yml`` file,
    and add a configuration variable to match your settings : ``disqus.shortname`` 
    
    To set developer mode on the site, set ``disqus.developer=1`` in your ``config.yml`` file.
    
    To prevent comments on a particular page, set ``disqus = no`` in the page's YAML preamble.

    :copyright: (c) 2012 by Martin Andrews.
    :license: BSD, see LICENSE for more details.
"""
import jinja2

@jinja2.contextfunction
def get_disqus(context):
    var_shortname = context['builder'].config.root_get('modules.disqus.shortname', 'YOUR-DISQUS-SHORTNAME')

    vars = []

    if context['config'].get('disqus_id', context['config'].get('post_id', None)):
        vars.append("var disqus_identifier = '%s';" % (
            context['config'].get('disqus_id',  # fall back to post_id if None
                context['config'].get('post_id', None)), ))

    if context['config'].get('disqus_url', None):
        vars.append("var disqus_url = '%s';" % (context['config'].get('disqus_url'), ))

    if context['builder'].config.root_get('modules.disqus.developer', False):
        vars.append("var disqus_developer = 1;")

    disqus_txt = """
<div id="disqus_thread"></div>
<script type="text/javascript">
    var disqus_shortname = '%s'; // required: replace example with your forum shortname
    %s
    
    /* * * DON'T EDIT BELOW THIS LINE * * */
    (function() {
        var dsq = document.createElement('script'); dsq.type = 'text/javascript'; dsq.async = true;
        dsq.src = ('https:' == document.location.protocol ? 'https://' : 'http://') + disqus_shortname + '.disqus.com/embed.js';
        (document.getElementsByTagName('head')[0] || document.getElementsByTagName('body')[0]).appendChild(dsq);
    })();
</script>
<noscript>Please enable JavaScript to view the <a href="http://disqus.com/?ref_noscript">comments powered by Disqus.</a></noscript>
<a href="http://disqus.com" class="dsq-brlink">blog comments powered by <span class="logo-disqus">Disqus</span></a>
""" % (var_shortname, '\n    '.join(vars), )

    if not context['config'].get('disqus', True):
        disqus_txt = ''

    return jinja2.Markup(disqus_txt.encode('utf-8'))


@jinja2.contextfunction
def get_disqus_count(context):
    var_shortname = context['builder'].config.root_get('modules.disqus.shortname', 'YOUR-DISQUS-SHORTNAME')
    disqus_txt = """
<script type="text/javascript">
    var disqus_shortname = '%s'; // required: replace example with your forum shortname

    /* * * DON'T EDIT BELOW THIS LINE * * */
    (function() {
        var cnt = document.createElement('script'); cnt.type = 'text/javascript'; cnt.async = true;
        cnt.src = ('https:' == document.location.protocol ? 'https://' : 'http://') + disqus_shortname + '.disqus.com/count.js';
        (document.getElementsByTagName('head')[0] || document.getElementsByTagName('body')[0]).appendChild(cnt);
    })();
</script>
<noscript>Please enable JavaScript to view the <a href="http://disqus.com/?ref_noscript">comments powered by Disqus.</a></noscript>
<a href="http://disqus.com" class="dsq-brlink">blog comments powered by <span class="logo-disqus">Disqus</span></a>
""" % (var_shortname, )

    if not context['config'].get('disqus', True):
        disqus_txt = ''

    return jinja2.Markup(disqus_txt.encode('utf-8'))


def setup(builder):
    builder.jinja_env.globals['get_disqus'] = get_disqus
    builder.jinja_env.globals['get_disqus_count'] = get_disqus_count

