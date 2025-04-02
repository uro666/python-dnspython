%define module dnspython
# disable tests on abf
%bcond_with test

Name:		python-dnspython
Version:	2.7.0
Release:	1
License:	ISC
URL:		https://www.dnspython.org/
Summary:	DNS toolkit for Python
Group:		Development/Python
Source0:	https://github.com/rthalley/dnspython/archive/refs/tags/%{module}-%{version}.tar.gz

BuildSystem: python
BuildArch:	noarch

BuildRequires: python
BuildRequires: pkgconfig(python3)
BuildRequires:	python%{pyver}dist(aioquic)
BuildRequires:	python%{pyver}dist(cryptography)
BuildRequires:	python%{pyver}dist(hatchling)
BuildRequires:	python%{pyver}dist(h2)
BuildRequires:	python%{pyver}dist(httpcore)
BuildRequires:	python%{pyver}dist(httpx)
BuildRequires:	python%{pyver}dist(idna)
BuildRequires:	python%{pyver}dist(poetry-core)
BuildRequires:	python%{pyver}dist(setuptools)
BuildRequires:	python%{pyver}dist(trio)
BuildRequires:	python%{pyver}dist(trio-websocket)
BuildRequires:	python%{pyver}dist(wheel)
Requires:	python%{pyver}dist(aioquic)
Requires:	python%{pyver}dist(cryptography)
Requires:	python%{pyver}dist(httpx)
Requires:	python%{pyver}dist(idna)
Recommends:	python%{pyver}dist(h2)
Suggests:	python%{pyver}dist(trio)
Suggests:	python%{pyver}dist(trio-websocket)

Provides:	dnspython = %{EVRD}
Provides:	dnspython3 = %{EVRD}
Obsoletes:	python2-dnspython < 2.7.0

%if %{with test}
BuildRequires:	python%{pyver}dist(black)
BuildRequires:	python%{pyver}dist(coverage)
BuildRequires:	python%{pyver}dist(flake8)
BuildRequires:	python%{pyver}dist(mypy)
BuildRequires:	python%{pyver}dist(pylint)
BuildRequires:	python%{pyver}dist(pytest)
BuildRequires:	python%{pyver}dist(pytest-asyncio)
BuildRequires:	python%{pyver}dist(pytest-trio)
BuildRequires:  python%{pyver}dist(requests)
BuildRequires:  python%{pyver}dist(requests-toolbelt)
BuildRequires:	python%{pyver}dist(twine)
%endif


%description
dnspython is a DNS toolkit for Python. It supports almost all record
types. It can be used for queries, zone transfers, and dynamic updates.
It supports TSIG authenticated messages and EDNS0.

dnspython provides both high and low level access to DNS. The high level
classes perform queries for data of a given name, type, and class, and
return an answer set. The low level classes allow direct manipulation
of DNS zones, messages, names, and records.


%prep
%autosetup -n %{module}-%{version} -p1
chmod -x examples/*

%build
%py_build

%install
%py_install

%if %{with test}
%check
# remove tests that require a working resolver and external DNS resolution
rm tests/test_async.py
rm tests/test_doh.py
rm tests/test_resolver.py
rm tests/test_resolver_override.py
ignore="not test_trio_inbound_xfr"

export NO_INTERNET=1
%{__python} -m pytest -v -k "not test_trio_inbound_xfr"
%endif

%files
%{python3_sitelib}/dns
%{python3_sitelib}/%{module}-%{version}.dist-info
%license LICENSE
