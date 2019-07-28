from _sha1 import sha1

from dominate import tags
from flask_bootstrap.nav import BootstrapRenderer
from flask_nav import Nav
from flask_nav.elements import Navbar, View

nav = Nav()


@nav.navigation()
def basenavbar():
    return Navbar(
        View('Logo', 'main.index'),
        View('Comparing Tool', 'main.compare'),
        View('Log In', 'auth.login')
    )


@nav.navigation()
def loggedinnavbar():
    return Navbar(
        View('Logo', 'main.index'),
        View('Comparing Tool', 'main.compare'),
        View('Admin Panel', 'admin.admin_home'),
        View('Log Out', 'auth.logout')
    )


@nav.renderer()
class InverseBootstrapRenderer(BootstrapRenderer):
    def visit_Navbar(self, node):
        node_id = self.id or sha1(str(id(node)).encode()).hexdigest()

        root = tags.nav() if self.html5 else tags.div(role='navigation')
        root['class'] = 'navbar navbar-inverse'

        cont = root.add(tags.div(_class='container-fluid'))

        header = cont.add(tags.div(_class='navbar-header'))
        btn = header.add(tags.button())
        btn['type'] = 'button'
        btn['class'] = 'navbar-toggle collapsed'
        btn['data-toggle'] = 'collapse'
        btn['data-target'] = '#' + node_id
        btn['aria-expanded'] = 'false'
        btn['aria-controls'] = 'navbar'

        btn.add(tags.span('Toggle navigation', _class='sr-only'))
        btn.add(tags.span(_class='icon-bar'))
        btn.add(tags.span(_class='icon-bar'))
        btn.add(tags.span(_class='icon-bar'))

        if node.title is not None:
            if hasattr(node.title, 'get_url'):
                header.add(tags.a(node.title.text, _class='navbar-brand',
                                  href=node.title.get_url()))
            else:
                header.add(tags.span(node.title, _class='navbar-brand'))

        bar = cont.add(tags.div(
            _class='navbar-collapse collapse',
            id=node_id,
        ))
        bar_list = bar.add(tags.ul(_class='nav navbar-nav'))

        for item in node.items:
            bar_list.add(self.visit(item))

        return root
