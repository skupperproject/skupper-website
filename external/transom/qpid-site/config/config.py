site_url = ""

class _Release(object):
    def __init__(self, site_url, component_name, component_key, number):
        self.site_url = site_url
        self.component_name = component_name
        self.component_key = component_key
        self.number = number

    @property
    def name(self):
        return "{} {}".format(self.component_name, self.number)

    @property
    def url(self):
        args = self.site_url, self.component_key, self.number
        return "{}/releases/{}-{}".format(*args)

    @property
    def link(self):
        return "<a href=\"{}\">{}</a>".format(self.url, self.name)

    @property
    def brief_link(self):
        return "<a href=\"{}\">{}</a>".format(self.url, self.number)

broker_j_release = _Release(site_url, "Qpid Broker-J", "qpid-broker-j", "9.2.1")
other_broker_j_release = None
cpp_release = _Release(site_url, "Qpid C++", "qpid-cpp", "1.39.0")
dispatch_release = _Release(site_url, "Qpid Dispatch", "qpid-dispatch", "1.19.0")
interop_test_release = _Release(site_url, "Qpid Interop Test", "qpid-interop-test", "0.3.0")
jms_release = _Release(site_url, "Qpid JMS", "qpid-jms", "2.7.0")
other_jms_release = "1.13.0"
jms_amqp_0_x_release = _Release(site_url, "Qpid JMS for AMQP 0-x", "qpid-jms-amqp-0-x", "6.4.0")
proton_release = _Release(site_url, "Qpid Proton", "qpid-proton", "0.40.0")
proton_j_release = _Release(site_url, "Qpid Proton-J", "qpid-proton-j", "0.34.1")
protonj2_release = _Release(site_url, "Qpid ProtonJ2", "qpid-protonj2", "1.0.0-M23")
python_release = _Release(site_url, "Qpid Python", "qpid-python", "1.37.0")
proton_dotnet_release = _Release(site_url, "Qpid Proton DotNet", "qpid-proton-dotnet", "1.0.0-M11")

current_broker_j_release = broker_j_release.number
current_broker_j_release_url = broker_j_release.url
current_broker_j_release_link = broker_j_release.link

current_cpp_release = cpp_release.number
current_cpp_release_url = cpp_release.url
current_cpp_release_link = cpp_release.link

current_dispatch_release = dispatch_release.number
current_dispatch_release_url = dispatch_release.url
current_dispatch_release_link = dispatch_release.link

current_interop_test_release = interop_test_release.number
current_interop_test_release_url = interop_test_release.url
current_interop_test_release_link = interop_test_release.link

current_jms_release = jms_release.number
current_jms_release_url = jms_release.url
current_jms_release_link = jms_release.link

current_jms_amqp_0_x_release = jms_amqp_0_x_release.number
current_jms_amqp_0_x_release_url = jms_amqp_0_x_release.url
current_jms_amqp_0_x_release_link = jms_amqp_0_x_release.link

current_proton_release = proton_release.number
current_proton_release_url = proton_release.url
current_proton_release_link = proton_release.link

current_proton_j_release = proton_j_release.number
current_proton_j_release_url = proton_j_release.url
current_proton_j_release_link = proton_j_release.link

current_protonj2_release = protonj2_release.number
current_protonj2_release_url = protonj2_release.url
current_protonj2_release_link = protonj2_release.link

current_python_release = python_release.number
current_python_release_url = python_release.url
current_python_release_link = python_release.link

current_proton_dotnet_release = proton_dotnet_release.number
current_proton_dotnet_release_url = proton_dotnet_release.url
current_proton_dotnet_release_link = proton_dotnet_release.link

def dashboard_asf_jira_links(project_key, project_id, components=None):
    try:
        from urllib.parse import quote_plus as url_escape
    except ImportError:
        from urllib import quote_plus as url_escape

    links = []

    all_issues_jql = "project = {}".format(project_key)
    open_issues_jql = all_issues_jql + " and resolution is null"

    if components is not None:
        components = ", ".join(["\"{}\"".format(x) for x in components])
        constraint = " and component in ({})".format(components)
        open_issues_jql += constraint
        all_issues_jql += constraint

    summary_url = "https://issues.apache.org/jira/projects/{}".format(project_key)
    open_issues_url = "https://issues.apache.org/jira/issues/?jql={}".format(url_escape(open_issues_jql))
    all_issues_url = "https://issues.apache.org/jira/issues/?jql={}".format(url_escape(all_issues_jql))
    create_issue_url = "https://issues.apache.org/jira/secure/CreateIssue!default.jspa?pid={}".format(project_id)

    links.append("<a href=\"{}\">Summary</a>".format(summary_url))
    links.append("<a href=\"{}\">Open issues</a>".format(open_issues_url))
    links.append("<a href=\"{}\">All issues</a>".format(all_issues_url))
    links.append("<a href=\"{}\">Create issue</a>".format(create_issue_url))

    return " &#x2022; ".join(links)

def dashboard_asf_git_links(repo_key):
    links = []

    git_url = "https://gitbox.apache.org/repos/asf/{}.git".format(repo_key)
    github_url = "https://github.com/apache/{}".format(repo_key)

    links.append("<a href=\"{}\">Git</a>".format(git_url))
    links.append("<a href=\"{}\">GitHub</a>".format(github_url))

    return " &#x2022; ".join(links)

def appveyor_ci_badge(party_key, job_key, badge_key, branch="main"):
    job_url = "https://ci.appveyor.com/project/{}/{}/branch/{}".format(party_key, job_key, branch)
    image_url = "https://ci.appveyor.com/api/projects/status/{}?branch={}&svg=true".format(badge_key, branch)

    return "<a href=\"{}\"><img src=\"{}\" height=\"20\"/></a>".format(job_url, image_url)

def github_ci_badge(repo, branch="main", workflow="build.yml"):
    job_url = "https://github.com/apache/{}/actions".format(repo)
    image_url = "https://github.com/apache/{}/actions/workflows/{}/badge.svg?branch={}".format(repo, workflow, branch)

    return "<a href=\"{}\"><img src=\"{}\" height=\"20\"/></a>".format(job_url, image_url)

def asf_jenkins_badge(job_key):
    job_url = "https://builds.apache.org/blue/organizations/jenkins/Qpid%2F{}/activity".format(job_key)
    image_url = "https://builds.apache.org/buildStatus/icon?job=Qpid/{}".format(job_key)

    return "<a href=\"{}\"><img src=\"{}\" height=\"20\"/></a>".format(job_url, image_url)

def asf_jenkins_pipeline_badge(job_key, branch="main"):
    job_url = "https://builds.apache.org/blue/organizations/jenkins/Qpid%2F{}/activity".format(job_key)
    image_url = "https://builds.apache.org/buildStatus/icon?job=Qpid/{}/{}".format(job_key, branch)

    return "<a href=\"{}\"><img src=\"{}\" height=\"20\"/></a>".format(job_url, image_url)
