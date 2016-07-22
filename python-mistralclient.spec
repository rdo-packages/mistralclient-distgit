Name:    python-mistralclient
Version: XXX
Release: XXX
Summary: Python API and CLI for OpenStack Mistral

Group:   Development/Languages
License: ASL 2.0
URL:     http://pypi.python.org/pypi/python-mistralclient
Source0: http://tarballs.openstack.org/%{name}/%{name}-%{version}.tar.gz

BuildArch: noarch

BuildRequires: python2-devel
BuildRequires: python-setuptools
BuildRequires: python-d2to1
BuildRequires: python-pbr

Requires: python-keystoneclient
Requires: python-pbr
Requires: python-osprofiler
Requires: python-six
Requires: PyYAML
Requires: python-requests

%description
This is a client for the OpenStack Mistral API. There's a Python API (the
mistralclient module), and a command-line script (mistral). Each implements 100% of
the OpenStack Mistral API.

%package doc
Summary: Documentation for OpenStack Mistral API Client
Group:   Documentation

BuildRequires: python-sphinx
BuildRequires: python-oslo-sphinx
BuildRequires: git

%description doc
This is a client for the OpenStack Mistral API. There's a Python API (the
mistralclient module), and a command-line script (mistral). Each implements 100% of
the OpenStack Mistral API.

This package contains auto-generated documentation.

%prep
%setup -q -n %{name}-%{upstream_version}

# Remove the requirements file so that pbr hooks don't add it
# to distutils requires_dist config.
rm -rf {test-,}requirements.txt tools/{pip,test}-requires

%build
%{__python2} setup.py build

%install
%{__python2} setup.py install -O1 --skip-build --root %{buildroot}
echo "%{version}" > %{buildroot}%{python2_sitelib}/mistralclient/versioninfo

# Install bash completion scripts
mkdir -p %{buildroot}%{_sysconfdir}/bash_completion.d/
install -m 644 -T tools/mistral.bash_completion %{buildroot}%{_sysconfdir}/bash_completion.d/python-mistralclient

# Delete tests
rm -fr %{buildroot}%{python2_sitelib}/mistralclient/tests

export PYTHONPATH="$( pwd ):$PYTHONPATH"
sphinx-build -b html doc/source html

# Fix hidden-file-or-dir warnings
rm -fr html/.doctrees html/.buildinfo

%files
%doc LICENSE README.rst
%{_bindir}/mistral
%{python2_sitelib}/mistralclient
%{python2_sitelib}/*.egg-info
%{_sysconfdir}/bash_completion.d/python-mistralclient

%files doc
%doc html

%changelog
# REMOVEME: error caused by commit 
