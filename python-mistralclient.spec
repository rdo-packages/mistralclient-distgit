%global pypi_name mistralclient

%{!?python2_shortver: %global python2_shortver %(%{__python2} -c 'import sys; print(str(sys.version_info.major) + "." + str(sys.version_info.minor))')}

%if 0%{?fedora}
%global with_python3 0
%{!?python3_shortver: %global python3_shortver %(%{__python3} -c 'import sys; print(str(sys.version_info.major) + "." + str(sys.version_info.minor))')}
%endif

%{!?upstream_version: %global upstream_version %{version}%{?milestone}}

Name:           python-%{pypi_name}
Version:        2.0.0
Release:        2%{?dist}
Summary:        Python client for Mistral REST API

License:        ASL 2.0
URL:            http://pypi.python.org/pypi/%{name}
Source0:        http://pypi.python.org/packages/source/p/%{name}/%{name}-%{version}.tar.gz

BuildArch:      noarch

%description
Python client for Mistral REST API. Includes python library for Mistral API
and Command Line Interface (CLI) library.


%package -n     python2-%{pypi_name}

BuildRequires:  python2-devel
BuildRequires:  python-setuptools
BuildRequires:  python-pbr

Requires:       python-cliff >= 1.14
Requires:       python-keystoneclient >= 1.6.0
Requires:       python-openstackclient >= 1.5.0
Requires:       python-pbr
Requires:       python-requests >= 2.5.2
Requires:       PyYAML >= 3.1.0

Summary:        Python client for Mistral REST API
%{?python_provide:%python_provide python2-%{pypi_name}}

%description -n python2-%{pypi_name}
Python client for Mistral REST API. Includes python library for Mistral API
and Command Line Interface (CLI) library.


# Python3 package
%if 0%{?with_python3}
%package -n     python3-%{pypi_name}
Summary:        Python client for Mistral REST API
%{?python_provide:%python_provide python3-%{pypi_name}}

BuildRequires:  python3-devel
BuildRequires:  python3-setuptools
BuildRequires:  python3-pbr >= 0.6
BuildRequires:  python-tools

Requires:       python3-cliff >= 1.14
Requires:       python3-keystoneclient >= 1.6.0
Requires:       python3-openstackclient >= 1.5.0
Requires:       python3-pbr
Requires:       python3-requests >= 2.5.2
Requires:       PyYAML >= 3.1.0

%description -n python3-%{pypi_name}
Python client for Mistral REST API. Includes python library for Mistral API
and Command Line Interface (CLI) library.
%endif


# Documentation package
%package -n python-%{pypi_name}-doc
Summary:       Documentation for python client for Mistral REST API

BuildRequires: python-sphinx
BuildRequires: python-oslo-sphinx >= 2.3.0

%description -n python-%{pypi_name}-doc
Documentation for python client for Mistral REST API. Includes python library
for Mistral API and Command Line Interface (CLI) library.


%prep
%autosetup -n %{name}-%{upstream_version}
# Remove bundled egg-info
rm -rf %{pypi_name}.egg-info
# Let RPM handle the dependencies
rm -f test-requirements.txt requirements.txt

%if 0%{?with_python3}
rm -rf %{py3dir}
cp -a . %{py3dir}
2to3 --write --nobackups %{py3dir}
%endif


%build
%{__python2} setup.py build

%if 0%{?with_python3}
pushd %{py3dir}
LANG=en_US.UTF-8 %{__python3} setup.py build
popd
%endif

# generate html docs
sphinx-build doc/source html
# remove the sphinx-build leftovers
rm -rf html/.{doctrees,buildinfo}


%install
%if 0%{?with_python3}
pushd %{py3dir}
LANG=en_US.UTF-8 %{__python3} setup.py install --skip-build --root %{buildroot}
mv %{buildroot}%{_bindir}/%{pypi_name} %{buildroot}%{_bindir}/python3-%{pypi_name}
popd
%endif

%{__python2} setup.py install --skip-build --root %{buildroot}

# rename binaries, make compat symlinks
pushd %{buildroot}%{_bindir}
ln -s %{pypi_name} %{pypi_name}
for i in %{pypi_name}-{2,%{?python2_shortver}}; do
    ln -s %{pypi_name} $i
done
%if 0%{?with_python3}
for i in %{pypi_name}-{3,%{?python3_shortver}}; do
    ln -s  python3-%{pypi_name} $i
done
%endif
popd


%files -n python2-%{pypi_name}
%license LICENSE
%doc README.md
%{python2_sitelib}/%{pypi_name}
%{python2_sitelib}/python_%{pypi_name}-*-py?.?.egg-info
%{_bindir}/mistral*

# Files for python3
%if 0%{?with_python3}
%files -n python3-%{pypi_name}
%license LICENSE
%doc README.md
%{_bindir}/python3-mistral*
%{_bindir}/mistral*
%{python3_sitelib}/%{pypi_name}
%{python3_sitelib}/python_%{pypi_name}-%{version}-py?.?.egg-info
%endif

%files -n python-%{pypi_name}-doc
%doc html
%license LICENSE


%changelog
* Fri Apr 15 2016 Haïkel Guémar <hguemar@fedoraproject.org> - 2.0.0-2
- Resync w/ spec contributed by mflobo

* Wed Mar 23 2016 RDO <rdo-list@redhat.com> 2.0.0-0.1
-  Rebuild for Mitaka
