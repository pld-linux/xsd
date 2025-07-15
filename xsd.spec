Summary:	W3C XML schema to C++ data binding compiler
Summary(pl.UTF-8):	Kompilator schematów W3C XML do wiązań danych C++
Name:		xsd
Version:	4.0.0
Release:	3
Group:		Development/Tools
# Exceptions permit otherwise GPLv2 incompatible combination with ASL-licensed Xerces
License:	GPL v2 with FLOSS exceptions
Source0:	http://www.codesynthesis.com/download/xsd/4.0/%{name}-%{version}+dep.tar.bz2
# Source0-md5:	ae64d7fcd258addc9b045fe3f96208bb
# Sent suggestion to upstream via e-mail 20090707
Patch0:		%{name}-3.3.0-xsdcxx-rename.patch
URL:		http://www.codesynthesis.com/products/xsd/
BuildRequires:	boost-devel
BuildRequires:	iconv
BuildRequires:	libcutl-devel >= 1.8.0
BuildRequires:	libstdc++-devel >= 6:4.2
BuildRequires:	libxsd-frontend-devel >= 2.0.0
BuildRequires:	m4
BuildRequires:	rpm-build >= 4.6
BuildRequires:	xerces-c-devel >= 3.0.0
Requires:	libcutl >= 1.8.0
Requires:	libxsd-frontend >= 2.0.0
Requires:	xerces-c-devel >= 3.0.0
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
CodeSynthesis XSD is an open-source, cross-platform W3C XML Schema to
C++ data binding compiler. Provided with an XML instance specification
(XML Schema), it generates C++ classes that represent the given
vocabulary as well as parsing and serialization code. You can then
access the data stored in XML using types and functions that
semantically correspond to your application domain rather than dealing
with intricacies of reading and writing XML.

%description -l pl.UTF-8
CodeSynthesis XSD to mający otwarte źródła wieloplatformowy kompilator
schematów W3C XML do wiązań danych C++. Na podstawie specyfikacji
instancji XML (schematu XML) generuje klasy C++ reprezentujące podany
słownik, a także kod analizujący i serializujący. Następnie można
odwoływać się do danych zapisanych w XML-u przy użyciu typów i funkcji
semantycznie odpowiadających działaniu aplikacji, bez zajmowania się
skomplikowaniem odczytu i zapisu XML-a.

%package apidocs
Summary:	API documentation files for XSD
Summary(pl.UTF-8):	Dokumentacja API XSD
Group:		Documentation
BuildArch:	noarch

%description apidocs
This package contains API documentation for XSD.

%description apidocs -l pl.UTF-8
Dokumentacja API XSD.

%prep
%setup -q -n %{name}-%{version}+dep
cd xsd
%patch -P0 -p1
cd ..

echo 'libxsd_frontend_installed := y' > xsd/build/import/libxsd-frontend/configuration-dynamic.make

%build
%{__make} \
	CXX="%{__cxx}" \
	CPPFLAGS="%{rpmcppflags}" \
	CXXFLAGS="%{rpmcxxflags}" \
	LDFLAGS="%{rpmldflags}" \
	EXTERNAL_LIBCUTL=y \
	verbose=1

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	install_prefix="$RPM_BUILD_ROOT%{_prefix}" \
	EXTERNAL_LIBCUTL=y

# Split API documentation to -doc subpackage.
rm -rf apidocdir
install -d apidocdir
%{__mv} $RPM_BUILD_ROOT%{_docdir}/xsd/*.{xhtml,css} apidocdir/
%{__mv} $RPM_BUILD_ROOT%{_docdir}/xsd/cxx/ apidocdir/
%{__mv} $RPM_BUILD_ROOT%{_docdir}/xsd/ docdir/

# Convert to utf-8.
for file in docdir/NEWS; do
	%{__mv} $file timestamp
	iconv -f ISO-8859-1 -t UTF-8 -o $file timestamp
	touch -r timestamp $file
done

# Rename binary to xsdcxx to avoid conflicting with mono-web package.
# Sent suggestion to upstream via e-mail 20090707
# they will consider renaming in 4.0.0
%{__mv} $RPM_BUILD_ROOT%{_bindir}/xsd $RPM_BUILD_ROOT%{_bindir}/xsdcxx
%{__mv} $RPM_BUILD_ROOT%{_mandir}/man1/xsd.1 $RPM_BUILD_ROOT%{_mandir}/man1/xsdcxx.1

# Remove duplicate docs.
%{__rm} -r $RPM_BUILD_ROOT%{_docdir}/libxsd

# Remove Microsoft Visual C++ compiler helper files.
%{__rm} -r $RPM_BUILD_ROOT%{_includedir}/xsd/cxx/compilers

# Remove redundant PostScript files that rpmlint grunts about not being UTF8
# See: https://bugzilla.redhat.com/show_bug.cgi?id=502024#c27
# for Boris Kolpackov's explanation about those
find apidocdir -name "*.ps" | xargs %{__rm}
# Remove other unwanted crap
find apidocdir -name "*.doxygen" \
            -o -name "makefile" \
            -o -name "*.html2ps" | xargs %{__rm}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc docdir/*
%attr(755,root,root) %{_bindir}/xsdcxx
%{_includedir}/xsd
%{_mandir}/man1/xsdcxx.1*

%files apidocs
%defattr(644,root,root,755)
%doc apidocdir/*
