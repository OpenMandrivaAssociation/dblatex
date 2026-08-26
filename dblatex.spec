Summary:	DocBook to LaTeX/ConTeXt Publishing
Name:		dblatex
Version:	0.3.12
Release:	2
Group:		Publishing
License:	GPLv2+
Url:		https://dblatex.sourceforge.net/
Source0:	http://downloads.sourceforge.net/%{name}/%{name}3-%{version}.tar.bz2
Source1:	COPYING-docbook-xsl
Patch0:		dblatex-0.3.11-which-shutil.patch
Patch1:		dblatex-disable-debian.patch
Patch2:		dblatex-0.3.12-replace-imp-by-importlib.patch
Patch3:		dblatex-0.3.12-adjust-submodule-imports.patch
Patch4:		dblatex-0.3.12-syntax-warnings.patch
BuildArch:	noarch

BuildRequires:	python
BuildRequires:	python%{pyver}dist(setuptools)
BuildRequires:	imagemagick
BuildRequires:	xsltproc
# setup.py install probes latex/pdflatex/kpsewhich and a set of .sty files.
# Depend on the individual modules, not collection-latexrecommended: that
# collection is published but several of its own texlive() deps are not.
BuildRequires:	texlive(latex-bin)
BuildRequires:	texlive(makeindex)
BuildRequires:	texlive(collection-latex)
BuildRequires:	texlive(anysize)
BuildRequires:	texlive(appendix)
BuildRequires:	texlive(changebar)
BuildRequires:	texlive(fancybox)
BuildRequires:	texlive(fancyvrb)
BuildRequires:	texlive(float)
BuildRequires:	texlive(footmisc)
BuildRequires:	texlive(jknapltx)
BuildRequires:	texlive(listings)
BuildRequires:	texlive(multirow)
# overpic/pdfpages mass-rebuilds have not landed yet, so the published
# packages do not Provide texlive(name). Use the RPM names until they do.
BuildRequires:	texlive-overpic
BuildRequires:	texlive-pdfpages
BuildRequires:	texlive(subfigure)
BuildRequires:	texlive(stmaryrd)
BuildRequires:	texlive(titlesec)
BuildRequires:	texlive(wasysym)
Requires:	docbook-dtd44-xml
Requires:	docbook-dtd45-xml
Requires:	imagemagick
Requires:	transfig
Requires:	xsltproc
Requires:	texlive(latex-bin)
Requires:	texlive(makeindex)
Requires:	texlive(collection-latex)
Requires:	texlive(anysize)
Requires:	texlive(appendix)
Requires:	texlive(changebar)
Requires:	texlive(fancybox)
Requires:	texlive(fancyvrb)
Requires:	texlive(float)
Requires:	texlive(footmisc)
Requires:	texlive(jknapltx)
Requires:	texlive(listings)
Requires:	texlive(multirow)
Requires:	texlive-overpic
Requires:	texlive-pdfpages
Requires:	texlive(subfigure)
Requires:	texlive(stmaryrd)
Requires:	texlive(titlesec)
Requires:	texlive(wasysym)
# shipped copies of these are stripped at install; use the TeX Live ones
Requires:	texlive(bibtopic)
Requires:	texlive(enumitem)
Requires:	texlive(passivetex)
Requires:	texlive(ragged2e)
Requires:	texlive(xmltex)
Requires:	texlive(xetex)
# overpic -> eepic (epic.sty); default style uses Times/Helvetica/Courier
Requires:	texlive(eepic)
Requires:	texlive(times)
Requires:	texlive(helvetic)
Requires:	texlive(courier)

%description
dblatex is a program that transforms your SGML/XMLDocBook
documents to DVI, PostScript or PDF by translating them
into pure LaTeX as a first process.  MathML 2.0 markups
are supported, too. It started as a clone of DB2LaTeX.

%prep
%setup -qn %{name}3-%{version}
%autopatch -p1

%build
python setup.py build

%install
python setup.py install --root %{buildroot}
# these are already in TeX Live packages:
for file in bibtopic.sty enumitem.sty ragged2e.sty passivetex/; do
	rm -rf %{buildroot}%{_datadir}/dblatex/latex/misc/$file
done

mkdir -p %{buildroot}%{_datadir}/texmf-dist/tex/latex/dblatex
for file in ` find %{buildroot}%{_datadir}/dblatex/latex/ -name '*.sty' ` ; do
	mv $file %{buildroot}%{_datadir}/texmf-dist/tex/latex/dblatex/`basename $file`;
done

rm -rf %{buildroot}%{_datadir}/dblatex/latex/{misc,contrib/example,style}

mkdir -p %{buildroot}%{_sysconfdir}/dblatex
# shipped in %%docs
rm -rf %{buildroot}%{_datadir}/doc/

sed -e 's/\r//' xsl/mathml2/README > README-xsltml
touch -r xsl/mathml2/README README-xsltml
cp -p %{SOURCE1} COPYING-docbook-xsl
chmod +x %{buildroot}%{py_sitedir}/dbtexmf/dblatex/xetex/*.py

sed -i '1s|python3|python|' %{buildroot}%{_bindir}/dblatex

%files
%{_mandir}/man1/dblatex.1*
%doc COPYRIGHT docs/manual.pdf COPYING-docbook-xsl README-xsltml
%{py_sitedir}/dbtexmf/
%{py_sitedir}/dblatex-*.egg-info
%{_bindir}/dblatex
%{_datadir}/dblatex/
%{_datadir}/texmf-dist/tex/latex/dblatex/
%dir %{_sysconfdir}/dblatex
