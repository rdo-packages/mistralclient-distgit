%{!?sources_gpg: %{!?dlrn:%global sources_gpg 1} }
%global sources_gpg_sign 0x2426b928085a020d8a90d0d879ab7008d0896c8a
%global pypi_name mistralclient
%global cliname   mistral
%global with_doc 1


%{!?upstream_version: %global upstream_version %{version}%{?milestone}}

%global common_desc \
Python client for Mistral REST API. Includes python library for Mistral API \
and Command Line Interface (CLI) library.

Name:           python-%{pypi_name}
Version:        XXX
Release:        XXX
Summary:        Python client for Mistral REST API

License:        ASL 2.0
URL:            https://pypi.io/pypi/python-mistralclient
Source0:        https://tarballs.openstack.org/%{name}/%{name}-%{upstream_version}.tar.gz
# Required for tarball sources verification
%if 0%{?sources_gpg} == 1
Source101:        https://tarballs.openstack.org/%{name}/%{name}-%{upstream_version}.tar.gz.asc
Source102:        https://releases.openstack.org/_static/%{sources_gpg_sign}.txt
%endif

BuildArch:      noarch

# Required for tarball sources verification
%if 0%{?sources_gpg} == 1
BuildRequires:  /usr/bin/gpgv2
BuildRequires:  openstack-macros
%endif

%description
%{common_desc}

%package -n     python3-%{pypi_name}
Summary:        Python client for Mistral REST API
%{?python_provide:%python_provide python3-%{pypi_name}}
Obsoletes: python2-%{pypi_name} < %{version}-%{release}

BuildRequires:  python3-devel
BuildRequires:  python3-setuptools
BuildRequires:  python3-pbr
BuildRequires:  git-core

Requires:       python3-osc-lib >= 1.10.0
Requires:       python3-oslo-i18n >= 3.15.3
Requires:       python3-oslo-utils >= 3.33.0
Requires:       python3-oslo-serialization >= 2.18.0
Requires:       python3-pbr
Requires:       python3-requests >= 2.14.2
Requires:       python3-stevedore >= 1.20.0
Requires:       python3-keystoneauth1 >= 3.4.0
Requires:       python3-cliff >= 2.8.0

Requires:       python3-yaml >= 3.13


%description -n python3-%{pypi_name}
%{common_desc}

%if 0%{with_doc}
# Documentation package
%package -n python-%{pypi_name}-doc
Summary:       Documentation for python client for Mistral REST API

BuildRequires: python3-sphinx
BuildRequires: python3-openstackdocstheme
BuildRequires: python3-sphinxcontrib-apidoc
BuildRequires: python3-oslotest
BuildRequires: python3-stevedore
BuildRequires: python3-oslo-utils
BuildRequires: python3-oslo-i18n
BuildRequires: python3-osc-lib
BuildRequires: python3-cliff

BuildRequires: python3-PyYAML
BuildRequires: python3-requests-mock


%description -n python-%{pypi_name}-doc
%{common_desc}

This package contains documentation.
%endif

%prep
# Required for tarball sources verification
%if 0%{?sources_gpg} == 1
%{gpgverify}  --keyring=%{SOURCE102} --signature=%{SOURCE101} --data=%{SOURCE0}
%endif
%autosetup -n %{name}-%{upstream_version} -S git
# Remove bundled egg-info
rm -rf %{pypi_name}.egg-info
# Let RPM handle the dependencies
rm -f test-requirements.txt requirements.txt
# Remove the functional tests, we don't need them in the package
rm -rf mistralclient/tests/functional

%build
%{py3_build}

%if 0%{with_doc}
# generate html docs
sphinx-build-3 -b html doc/source doc/build/html
# remove the sphinx-build-3 leftovers
rm -rf doc/build/html/.{doctrees,buildinfo}
%endif

%install
%{py3_install}

# Create a versioned binary for backwards compatibility until everything is pure py3
ln -s %{cliname} %{buildroot}%{_bindir}/%{cliname}-3

# Install bash completion scripts
mkdir -p %{buildroot}%{_sysconfdir}/bash_completion.d/
install -m 644 -T tools/mistral.bash_completion %{buildroot}%{_sysconfdir}/bash_completion.d/python-mistralclient


%files -n python3-%{pypi_name}
%license LICENSE
%doc README.rst
%{python3_sitelib}/%{pypi_name}
%{python3_sitelib}/python_%{pypi_name}-*-py%{python3_version}.egg-info
%{_bindir}/%{cliname}
%{_bindir}/%{cliname}-3
%{_sysconfdir}/bash_completion.d/python-mistralclient


%if 0%{with_doc}
%files -n python-%{pypi_name}-doc
%doc doc/build/html
%license LICENSE
%endif


%changelog
