%global pypi_name mistralclient
%global cliname   mistral

%{!?python2_shortver: %global python2_shortver %(%{__python2} -c 'import sys; print(str(sys.version_info.major) + "." + str(sys.version_info.minor))')}

%if 0%{?fedora}
%global with_python3 1
%{!?python3_shortver: %global python3_shortver %(%{__python3} -c 'import sys; print(str(sys.version_info.major) + "." + str(sys.version_info.minor))')}
%endif

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

%package -n     python2-%{pypi_name}

BuildRequires:  python2-devel
BuildRequires:  python-setuptools
BuildRequires:  python-pbr
BuildRequires:  git

Requires:       python-cliff >= 2.8.0
Requires:       python-keystoneclient >= 1:3.8.0
Requires:       python-osc-lib >= 1.7.0
Requires:       python-oslo-i18n >= 2.1.0
Requires:       python-oslo-utils >= 3.20.0
Requires:       python-osprofiler
Requires:       python-pbr
Requires:       python-requests >= 2.10.0
Requires:       python-six >= 1.9.0
Requires:       python-stevedore >= 1.20.0
Requires:       PyYAML >= 3.10

Summary:        Python client for Mistral REST API
%{?python_provide:%python_provide python2-%{pypi_name}}

%description -n python2-%{pypi_name}
%{common_desc}


# Python3 package
%if 0%{?with_python3}
%package -n     python3-%{pypi_name}
Summary:        Python client for Mistral REST API
%{?python_provide:%python_provide python3-%{pypi_name}}

BuildRequires:  python3-devel
BuildRequires:  python3-setuptools
BuildRequires:  python3-pbr >= 0.6
BuildRequires:  python-tools

Requires:       python3-cliff >= 2.8.0
Requires:       python3-keystoneclient >= 1:3.8.0
Requires:       python3-osc-lib >= 1.7.0
Requires:       python3-oslo-i18n >= 2.1.0
Requires:       python3-oslo-utils >= 3.20.0
Requires:       python3-osprofiler
Requires:       python3-pbr
Requires:       python3-requests >= 2.10.0
Requires:       python3-six >= 1.9.0
Requires:       python3-stevedore >= 1.20.0
Requires:       python3-PyYAML >= 3.10

%description -n python3-%{pypi_name}
%{common_desc}
%endif


# Documentation package
%package -n python-%{pypi_name}-doc
Summary:       Documentation for python client for Mistral REST API

BuildRequires: python-sphinx
BuildRequires: python-openstackdocstheme
BuildRequires: PyYAML
BuildRequires: python-tempest
BuildRequires: python-oslotest
BuildRequires: python-cliff
BuildRequires: python-stevedore
BuildRequires: python-oslo-utils
BuildRequires: python-oslo-i18n
BuildRequires: python-osc-lib
BuildRequires: python-keystoneclient
BuildRequires: python-requests-mock
BuildRequires: python-osprofiler


%description -n python-%{pypi_name}-doc
%{common_desc}

This package contains documentation.

%prep
%autosetup -n %{name}-%{upstream_version} -S git
# Remove bundled egg-info
rm -rf %{pypi_name}.egg-info
# Let RPM handle the dependencies
rm -f test-requirements.txt requirements.txt

%build
%{__python2} setup.py build

%if 0%{?with_python3}
%py3_build
%endif

# generate html docs
%{__python2} setup.py build_sphinx -b html
# remove the sphinx-build leftovers
rm -rf doc/build/html/.{doctrees,buildinfo}

%install
%if 0%{?with_python3}
%py3_install
mv %{buildroot}%{_bindir}/%{cliname} %{buildroot}%{_bindir}/python3-%{cliname}
%endif

%{__python2} setup.py install --skip-build --root %{buildroot}

# rename binaries, make compat symlinks
pushd %{buildroot}%{_bindir}
for i in %{cliname}-{2,%{?python2_shortver}}; do
    ln -s %{cliname} $i
done
%if 0%{?with_python3}
for i in %{cliname}-{3,%{?python3_shortver}}; do
    ln -s  python3-%{cliname} $i
done
%endif
popd
# Install bash completion scripts
mkdir -p %{buildroot}%{_sysconfdir}/bash_completion.d/
install -m 644 -T tools/mistral.bash_completion %{buildroot}%{_sysconfdir}/bash_completion.d/python-mistralclient


%files -n python2-%{pypi_name}
%license LICENSE
%doc README.rst
%{python2_sitelib}/%{pypi_name}
%{python2_sitelib}/python_%{pypi_name}-*-py?.?.egg-info
%{_bindir}/mistral
%{_bindir}/mistral-2*
%{_sysconfdir}/bash_completion.d/python-mistralclient


# Files for python3
%if 0%{?with_python3}
%files -n python3-%{pypi_name}
%license LICENSE
%doc README.rst
%{_bindir}/python3-mistral*
%{_bindir}/mistral-3*
%{python3_sitelib}/%{pypi_name}
%{python3_sitelib}/python_%{pypi_name}-*-py?.?.egg-info
%endif

%files -n python-%{pypi_name}-doc
%doc doc/build/html
%license LICENSE


%changelog
