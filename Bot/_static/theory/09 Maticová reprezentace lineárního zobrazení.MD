# Maticová reprezentace lineárnı́ho zobrazenı́

## Maticová reprezentace lineárního zobrazení

* Cíl: Najít souřadnice vektoru _f(u)_ v bazi _F_, pokud známe souřadnice _u_ v bazi _E_
  * Zjistit, zdali obraz _f(u)_ vůbec existuje, může být problémové; problému se lze vyhnout, pokud se budeme zabývat pouze zobrazením _f<sub>|D(f)</sub>_ : _Ũ_(_D(f)_, ⊕<sub>u</sub>, ⊗<sub>u</sub>) → _V_ (zúžení na definiční obor)
* Matice _F<sub>E→F</sub>_ se nazývá maticová reprezentace lineárního zobrazení _f_ v bazích _E_ a _F_
  * Její rozměry jsou dim(_V_)×dim(_U_) (dimenze prostoru obrazů × dimenze prostoru vzorů)
* Pokud:
  * _U_=(_M_, ⊕<sub>u</sub>, ⊗<sub>u</sub>) a _V_=(_N_, ⊕<sub>v</sub>, ⊗<sub>v</sub>) jsou konečnorozměrné prostory
  * _E_ ⊂ _M_ a _F_ ⊂ _N_ jsou baze těchto prostorů
  * Zobrazení f : _U_ → _V_ je lineární
  * _D(f)_ = _M_
* pak existuje taková matice _F<sub>E→F</sub>_, že _(f(u))<sup>F</sup>_ = _F<sub>E→F</sub>_ ⋅ _u<sup>E</sup>_ pro každý vektor _u_ ∈ _M_
* Tato matice je určena jednoznačně
* Pro vytvoření matice _F<sub>E→F</sub>_ najdeme obrazy _f(e<sub>j</sub>)_ všech bazových vektorů baze _E_ a určíme jejich souřadnice v bazi _F_, ty ve správném pořadí zapíšeme po sloupcích do matice

### Hodnost matice

* Obor hodnot lineáního zobrazení tvoří podprostor v cílové množině, nazývá se hodnost zobrazení
  * rank(_f_) = dim(_W(f))_
* Každý vektor z _W(f)_ je lineární kombinací vektorů _f(e<sub>j</sub>)_
  * _W(f)_ = span(_{f(e<sub>j</sub>)}<sub>j=1..n</sub>_)
* Počet lineárně nezávislých sloupců/řádků matice se nazývá hodnost matice

### Maticové reprezentace operací

* Maticovou reprezentací identity ve stejných bazích je jednotková matice
  * Identita v různých bazích je pak matice přechodu
* Maticová reprezentace lineární kombinace lineárních zobrazení je lineární kombinací maticových reprezentací původních zobrazení (ve stejných bazích se stejnými koeficienty)
* Maticová reprezentace složeného lineárního zobrazení je součinem maticových reprezentací jednotlivých zobrazení
* Maticová reprezentace případného inverzního lineárního zobrazení je rovna inverzní matici reprezentující původní lineární zobrazení (v&nbsp;příslušných bazích obou prostorů)
