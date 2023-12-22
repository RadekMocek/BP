# Lineárnı́ závislost vektorů

## Lineární závislost

* Množina vektorů _A_ = {_a<sub>1</sub>_, _a<sub>2</sub>_, (...)} je lineárně závislá, pokud existuje vektor _a<sub>j</sub>_ ∈ _A_, který je lineární kombinací **ostatních** vektorů z _A_
* Množina je lineárně nezávislá, pokud se žádný její vektor nedá vyjádřit jako lineární kombinace těch ostatních
* Je-li množina _A_ lineárně závislá ⟺ existuje netriviální lineární kombinace jejích vektorů, která dá nulový vektor
* Je-li množina _A_ lineárně nezávislá ⟺ jediná lineární kombinace, která dá nulový vektor, je ta triviální (všechny koeficienty jsou nulové)
* Každá množina, která obsahuje nulový vektor _o_ a k tomu ještě nějaký další vektor, je lineárně závislá
* Nenulové _n_-tice čísel tvořící řádky matice, která je ve horním stupňovitém tvaru, jsou lineárně nezávislé

## Baze vektorového prostoru

* Je-li _V_=(_M_, ⊕, ⊗) vektorový prostor a _A_ ⊂ _M_ taková **lineárně nezávislá** množina, že **span(_A_) = _M_**, nazveme _A_ **bazí** prostoru _V_
  * tzn.: _A_ je bazí prostoru _V_=(_M_, ⊕, ⊗), pokud je každý vektor z množiny _M_ dosažitelný lineární kombinací vektorů z množiny _A_ a zároveň jsou vektory z množiny _A_ lineárně nezávislé
  * `B1` Každý vektor z _M_ je lineární kombinací vektorů z _A_
  * `B2` Pokud z _A_ vynecháme nějaký vektor _a<sub>j</sub>_, pak přestane platit tvrzení `B1`
  * (Jedná se tedy o jednu z řady nejmenších množin, která splňuje tvrzení `B1` → generuje prostor _V_)
* Baze je uspořádaná → záleží na pořadí
* Nejobvyklejší baze se označují jako kanonické
  * např. v prostoru ℝ<sup>3</sup> by se jednalo o vektory (1, 0, 0), (0, 1, 0) a (0, 0, 1)

## Dimenze vektorového prostoru

* Steinitzova věta: Každé dvě (⟹ všechny) baze téhož vektorového prostoru mají stejný počet prvků
  * Počet prvků není tedy vlastností baze, ale prostoru, říká se jí dimenze (rozměr) vektorového prostoru
* Dimenze vektorového prostoru je tedy počet prvků jeho libovolné baze
* Pokud baze neexistuje pak dim(_V_) = ∞

## Souřadnice vektoru v bazi

* Je-li  _E_={_e<sub>j</sub>_} baze vektorového prostoru _V_=(_M_, ⊕, ⊗) a vektor _u_ ∈ _M_, pak jsou koeficienty této lineární kombinace jednoznačné:

$$$render
u=\bigoplus_{j=1}^k(\alpha_j\otimes e_j)
$$

* Koeficienty této lineární kombinace nazveme souřadnicemi vektoru _u_ v bazi _E_
* Týž vektor má v různých bazích obecně různé souřadnice
* Pro _V_=(_M_, ⊕, ⊗) nad _T_ s bazí _E_, kde dim(_V_) = _n_:
  * Pro souřadnice vektoru _w_ = _u_ ⊕ _v_ v bazi _E_ platí _w<sup>E</sup>_ = _u<sup>E</sup>_ ⊕ _v<sup>E</sup>_ ve smyslu sčítání vektorů z _T<sup>n</sup>_
  * Pro souřadnice vektoru _w_ = _α_ ⊗ _u_ v bazi _E_ platí _w<sup>E</sup>_ = _α_ ⊗ _u<sup>E</sup>_ ve smyslu násobku vektoru z _T<sup>n</sup>_

### Souřadnice vektoru jako vektor

* O souřadnicích se dá uvažovat také jako o vektorech
* Souřadnice součtu vektorů dostaneme sčítáním souřadnic jednotlivých vektorů
* a souřadnice násobku vektoru jsou násobkem souřadnic vektoru (vše musí být ve stejné bazi, bez ohledu na původní vektorový prostor)
* ⟹ Je-li v _n_-rozměrném prostoru _V_ k dispozici nějaká baze, můžeme práci s vektory z prostoru _V_ nahradit prací s _n_-ticemi čísel
* ⟹ Prostory _V_ nad _T_ kde dim(_V_) = _n_ a prostory _T<sup>n</sup>_ jsou izomorfní
* ⟹ Každé dva prostory nad stejným tělesem a se stejnou konečnou dimenzí jsou navzájem izomorfní

### Přiřazení souřadnic a vektorů

* Zobrazení, která přiřazují vektorům jejich souřadnice v určité bazi, jsou prostá
  * Souřadnice vektoru _u_ v bazi _E_ značíme _u<sup>E</sup>_
* Díky prostotě existují inverzní zobrazení, která souřadnicím v dané bazi přiřazují vektory
* Přiřazení souřadnic k vektoru _u_ v bazi _E_ značíme jako s<sub>E</sub>(_u_) a přiřazení vektoru k souřadnicím jako v<sub>E</sub>(_u<sup>E</sup>_)
  * _u<sup>E</sup>_ = s<sub>E</sub>(_u_)
  * _u_ = v<sub>E</sub>(_u<sup>E</sup>_)
