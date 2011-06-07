Name:		dblatex
Version:	0.3
Release:	%mkrel 4
Summary:	DocBook to LaTeX/ConTeXt Publishing
BuildArch:	noarch
Group:		Publishing
License:	GPLv2+
URL:		http://dblatex.sourceforge.net/
Source0:	http://downloads.sourceforge.net/dblatex/dblatex-%{version}.tar.bz2
#Source1:        http://docbook.sourceforge.net/release/xsl/current/COPYING
Source1:        COPYING-docbook-xsl
Patch0:		dblatex-0.2.7-external-which.patch
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root

%py_requires -d
BuildRequires:	libxslt-proc tetex imagemagick tetex-latex python-which
Requires:	tetex libxslt-proc docbook-dtd44-xml docbook-dtd45-xml xmltex tetex-latex imagemagick transfig
#BuildRequires:  tetex-fonts
Requires(post): tetex
Requires(postun): tetex

%description
dblatex is a program that transforms your SGML/XMLDocBook
documents to DVI, PostScript or PDF by translating them
into pure LaTeX as a first process.  MathML 2.0 markups
are supported, too. It started as a clone of DB2LaTeX.

Authors:
--------
   Benoît Guillon <marsgui at users dot sourceforge dot net>
   Andreas Hoenen <andreas dot hoenen at arcor dot de>


%prep
%setup -q
%patch0 -p1 -b .external-which
rm -r lib/contrib

%build
%{__python} setup.py build


%install
rm -rf $RPM_BUILD_ROOT
#%{__python} setup.py install --skip-build --root $RPM_BUILD_ROOT
%{__python} setup.py install --root $RPM_BUILD_ROOT
# these are already in tetex-latex:
for file in bibtopic.sty enumitem.sty ragged2e.sty passivetex/; do
  rm -rf $RPM_BUILD_ROOT%{_datadir}/dblatex/latex/misc/$file
done

mkdir -p $RPM_BUILD_ROOT%{_datadir}/texmf/tex/latex/dblatex
for file in ` find $RPM_BUILD_ROOT%{_datadir}/dblatex/latex/ -name '*.sty' ` ; do 
  mv $file $RPM_BUILD_ROOT%{_datadir}/texmf/tex/latex/dblatex/`basename $file`;
done

rm -rf $RPM_BUILD_ROOT%{_datadir}/dblatex/latex/{misc,contrib/example,style}

mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/dblatex
# shipped in %%docs
rm -rf $RPM_BUILD_ROOT%{_datadir}/doc/

sed -e 's/\r//' xsl/mathml2/README > README-xsltml
touch -r xsl/mathml2/README README-xsltml
cp -p %{SOURCE1} COPYING-docbook-xsl

 
%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr(-,root,root,-)
%{_mandir}/man1/dblatex.1*
%doc COPYRIGHT docs/manual.pdf COPYING-docbook-xsl README-xsltml
%{python_sitelib}/dbtexmf/
%{python_sitelib}/dblatex-*.egg-info
%{_bindir}/dblatex
%{_datadir}/dblatex/
%{_datadir}/texmf/tex/latex/dblatex/
%dir %{_sysconfdir}/dblatex

%post -p /usr/bin/texhash

%postun -p /usr/bin/texhash

