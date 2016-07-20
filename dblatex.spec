Summary:	DocBook to LaTeX/ConTeXt Publishing
Name:		dblatex
Version:	0.3.7
Release:	1
Group:		Publishing
License:	GPLv2+
Url:		http://dblatex.sourceforge.net/
Source0:	http://downloads.sourceforge.net/dblatex/dblatex-%{version}.tar.bz2
Source1:	COPYING-docbook-xsl
Patch0:		dblatex-0.2.7-external-which.patch
Patch1:		dblatex-disable-debian.patch
BuildArch:	noarch

BuildRequires:	python2-devel
BuildRequires:	python2-setuptools
BuildRequires:	imagemagick
BuildRequires:	python-which
BuildRequires:	tetex
BuildRequires:	tetex-latex
BuildRequires:	texlive-latex-bin
BuildRequires:	xsltproc
Requires:	docbook-dtd44-xml
Requires:	docbook-dtd45-xml
Requires:	imagemagick
Requires:	tetex
Requires:	tetex-latex
Requires:	texlive-latex-bin
Requires:	transfig
Requires:	xmltex
Requires:	xsltproc
Requires(post,postun):	kpathsea

%description
dblatex is a program that transforms your SGML/XMLDocBook
documents to DVI, PostScript or PDF by translating them
into pure LaTeX as a first process.  MathML 2.0 markups
are supported, too. It started as a clone of DB2LaTeX.

%prep
%setup -q
%apply_patches

%build
%{__python2} setup.py build

%install
%{__python2} setup.py install --root %{buildroot}
# these are already in tetex-latex:
for file in bibtopic.sty enumitem.sty ragged2e.sty passivetex/; do
	rm -rf %{buildroot}%{_datadir}/dblatex/latex/misc/$file
done

mkdir -p %{buildroot}%{_datadir}/texmf/tex/latex/dblatex
for file in ` find %{buildroot}%{_datadir}/dblatex/latex/ -name '*.sty' ` ; do 
	mv $file %{buildroot}%{_datadir}/texmf/tex/latex/dblatex/`basename $file`;
done

rm -rf %{buildroot}%{_datadir}/dblatex/latex/{misc,contrib/example,style}

mkdir -p %{buildroot}%{_sysconfdir}/dblatex
# shipped in %%docs
rm -rf %{buildroot}%{_datadir}/doc/

sed -e 's/\r//' xsl/mathml2/README > README-xsltml
touch -r xsl/mathml2/README README-xsltml
cp -p %{SOURCE1} COPYING-docbook-xsl
chmod +x %{buildroot}/%{py2_puresitedir}/dbtexmf/dblatex/xetex/*.py

sed -i 's|python|python2|' %{buildroot}/%{_bindir}/dblatex

%post
/usr/bin/texhash

%postun
/usr/bin/texhash

%files
%{_mandir}/man1/dblatex.1*
%doc COPYRIGHT docs/manual.pdf COPYING-docbook-xsl README-xsltml
%{python2_sitelib}/dbtexmf/
%{python2_sitelib}/dblatex-*.egg-info
%{_bindir}/dblatex
%{_datadir}/dblatex/
%{_datadir}/texmf/tex/latex/dblatex/
%dir %{_sysconfdir}/dblatex
