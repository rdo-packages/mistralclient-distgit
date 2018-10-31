# Macros for py2/py3 compatibility
%if 0%{?fedora} || 0%{?rhel} > 7
%global pyver %{python3_pkgversion}
%else
%global pyver 2
%endif
%global pyver_bin python%{pyver}
%global pyver_sitelib %python%{pyver}_sitelib
%global pyver_install %py%{pyver}_install
%global pyver_build %py%{pyver}_build
# End of macros for py2/py3 compatibility
%global pypi_name mistralclient
%global cliname   mistral


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

BuildArch:      noarch

%description
%{common_desc}

%package -n     python%{pyver}-%{pypi_name}
Summary:        Python client for Mistral REST API
%{?python_provide:%python_provide python%{pyver}-%{pypi_name}}
%if %{pyver} == 3
Obsoletes: python2-%{pypi_name} < %{version}-%{release}
%endif

BuildRequires:  python%{pyver}-devel
BuildRequires:  python%{pyver}-setuptools
BuildRequires:  python%{pyver}-pbr
BuildRequires:  git

Requires:       python%{pyver}-osc-lib >= 1.10.0
Requires:       python%{pyver}-oslo-i18n >= 3.15.3
Requires:       python%{pyver}-oslo-utils >= 3.33.0
Requires:       python%{pyver}-oslo-serialization >= 2.18.0
Requires:       python%{pyver}-osprofiler
Requires:       python%{pyver}-pbr
Requires:       python%{pyver}-requests >= 2.14.2
Requires:       python%{pyver}-six >= 1.10.0
Requires:       python%{pyver}-stevedore >= 1.20.0
Requires:       python%{pyver}-keystoneauth1 >= 3.4.0
Requires:       python%{pyver}-cliff >= 2.8.0

# Handle python2 exception
%if %{pyver} == 2
Requires:       PyYAML >= 3.10
%else
Requires:       python%{pyver}-PyYAML >= 3.10
%endif


%description -n python%{pyver}-%{pypi_name}
%{common_desc}

# Documentation package
%package -n python-%{pypi_name}-doc
Summary:       Documentation for python client for Mistral REST API

BuildRequires: python%{pyver}-sphinx
BuildRequires: python%{pyver}-openstackdocstheme
BuildRequires: python%{pyver}-oslotest
BuildRequires: python%{pyver}-stevedore
BuildRequires: python%{pyver}-oslo-utils
BuildRequires: python%{pyver}-oslo-i18n
BuildRequires: python%{pyver}-osc-lib
BuildRequires: python%{pyver}-osprofiler
BuildRequires: python%{pyver}-cliff

# Handle python2 exception
%if %{pyver} == 2
BuildRequires: PyYAML
BuildRequires: python-requests-mock
%else
BuildRequires: python%{pyver}-PyYAML
BuildRequires: python%{pyver}-requests-mock
%endif


%description -n python-%{pypi_name}-doc
%{common_desc}

This package contains documentation.

%prep
%autosetup -n %{name}-%{upstream_version} -S git
# Remove bundled egg-info
rm -rf %{pypi_name}.egg-info
# Let RPM handle the dependencies
rm -f test-requirements.txt requirements.txt
# Remove the functional tests, we don't need them in the package
rm -rf mistralclient/tests/functional

%build
%{pyver_build}

# generate html docs
%{pyver_bin} setup.py build_sphinx -b html
# remove the sphinx-build-%{pyver} leftovers
rm -rf doc/build/html/.{doctrees,buildinfo}

%install
%{pyver_install}

# Create a versioned binary for backwards compatibility until everything is pure py3
ln -s %{cliname} %{buildroot}%{_bindir}/%{cliname}-%{pyver}

# Install bash completion scripts
mkdir -p %{buildroot}%{_sysconfdir}/bash_completion.d/
install -m 644 -T tools/mistral.bash_completion %{buildroot}%{_sysconfdir}/bash_completion.d/python-mistralclient


%files -n python%{pyver}-%{pypi_name}
%license LICENSE
%doc README.rst
%{pyver_sitelib}/%{pypi_name}
%{pyver_sitelib}/python_%{pypi_name}-*-py?.?.egg-info
%{_bindir}/%{cliname}
%{_bindir}/%{cliname}-%{pyver}
%{_sysconfdir}/bash_completion.d/python-mistralclient


%files -n python-%{pypi_name}-doc
%doc doc/build/html
%license LICENSE


%changelog
