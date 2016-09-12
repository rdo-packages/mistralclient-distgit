%{!?upstream_version: %global upstream_version %{version}%{?milestone}}
Name:    python-mistralclient
Version: 2.1.1
Release: 1%{?dist}
Summary: Python API and CLI for OpenStack Mistral

Group:   Development/Languages
License: ASL 2.0
URL:     https://pypi.io/pypi/python-mistralclient
Source0: http://tarballs.openstack.org/%{name}/%{name}-%{upstream_version}.tar.gz

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
%doc README.rst
%license LICENSE
%{_bindir}/mistral
%{python2_sitelib}/mistralclient
%{python2_sitelib}/*.egg-info
%{_sysconfdir}/bash_completion.d/python-mistralclient

%files doc
%doc html

%changelog
* Tue Sep 13 2016 Haikel Guemar <hguemar@fedoraproject.org> 2.1.1-1
- Update to 2.1.1

