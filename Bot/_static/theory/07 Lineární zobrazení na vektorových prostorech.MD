# Lineárnı́ zobrazenı́ na vektorových prostorech

## Lineární zobrazení

* Jsou-li _U_=(_M_, ⊕<sub>u</sub>, ⊗<sub>u</sub>), _V_=(_N_, ⊕<sub>v</sub>, ⊗<sub>v</sub>) vektorové prostory nad tělesem _T_ a _f_ zobrazení _M_ → _N_, řekneme, že zobrazení _f_ je lineární, pokud platí:

1. ` Aditivní zobrazení:` **_f_(_u_ ⊕<sub>u</sub> _v_) = _f_(_u_) ⊕<sub>v</sub> _f_(_v_)**
2. `Homogenní zobrazení:` **_f_(_α_ ⊗<sub>u</sub> _v_) = _α_ ⊗<sub>v</sub> _f_(_u_)**

* (Pro všechna _u_, _v_ ∈ _M_, _α_ ∈ _T_)
* Pokud je zobrazení současně aditivní i homogenní ⟺ je lineární
* Lze také zapsat do jedné podmínky jako:
  * _f_((_α_ ⊗<sub>u</sub> _u_) ⊕<sub>u</sub> (_β_ ⊗<sub>u</sub> _v_)) = (_α_ ⊗<sub>v</sub> _f_(_u_)) ⊕<sub>v</sub> (_β_ ⊗<sub>v</sub> _f_(_v_))

### Známá lineární zobrazení

* Násobení matice <i>m</i>×<i>n</i> vektory z _T<sup>n</sup>_ je lineární zobrazení _T<sup>n</sup>_ → _T<sup>m</sup>_
* Přiřazení souřadnic v dané bazi k vektoru z _n_-rozměrného prostoru _V_ je lineární zobrazení _V_ → _T<sup>n</sup>_
  * I opačné přiřazení vektoru z _n_-rozměrného prostoru _V_ k souřadnicím v dané bazi je lineární zobrazení _T<sup>n</sup>_ → _V_
* Obecně každý izomorfismus dvojice vektorových prostorů _U_ a _V_ je lineární zobrazení _U_ → _V_ i _V_ → _U_
* Identita na libovolném vektorovém prostoru _V_ je lineární zobrazení _V_ → _V_
* Na prostoru orientovaných úseček v rovině jsou lineární zobrazení např. rotace o pevně daný úhel, zkosení, projekce, ... (podobná existují i pro orientované úsečky v prostoru)

## Definiční obor lineárního zobrazení

* Je-li _U_=(_M_, ⊕<sub>u</sub>, ⊗<sub>u</sub>) a zobrazení _f_ : _U_ → _V_ lineární, pak (_D(f)_, ⊕<sub>u</sub>, ⊗<sub>u</sub>) je podprostor v _U_

## Obor hodnot lineárního zobrazení

* Je-li _V_=(_N_, ⊕<sub>v</sub>, ⊗<sub>v</sub>) a zobrazení _f_ : _U_ → _V_ lineární, pak (_W(f)_, ⊕<sub>v</sub>, ⊗<sub>v</sub>) je podprostor v _V_
* Hodností lineárního zobrazení _f_ : _U_ → _V_ nazýváme dimenzi jeho oboru hodnot
  * rank(_f_) = dim(_W(f)_)
* Pokud je zobrazení lineární ⟹ obrazem nulového vektoru je vždy nulový vektor
  * _f(o<sub>u</sub>)_ = _f_(0 ⊗<sub>u</sub> _u_) = 0 ⊗<sub>v</sub> _f(u)_ = _o<sub>v</sub>_

## Jádro lineárního zobrazení

* Je-li _U_=(_M_, ⊕<sub>u</sub>, ⊗<sub>u</sub>) a zobrazení _f_ : _U_ → _V_ lineární, nazveme množinu všech vektorů z _U_, jejichž obrazem je nulový vektor, jádrem lineárního zobrazení _f_
  * ker(_f_) = {_x_ ∈ _D(f)_ : _f(x)_ = _o<sub>v</sub>_}
  * Jádro tohoto zobrazení je podprostorem v _U_ i v _D(f)_

## Linearita lineární kombinace

* Lineární kombinace lineárních zobrazení je lineární zobrazení (vše nad stejným tělesem)

## Linearita složeného zobrazení

* Složené zobrazení lineárních zobrazení je lineární zobrazení

## Linearita inverzního zobrazení

* Inverzní zobrazení k prostému lineárnímu zobrazení je také lineární

## Zúžení lineárního zobrazení

* Je-li _f_ : _U_=(_M_, ⊕, ⊗) → _V_=(_N_, ⊕, ⊗) lineární zobrazení a _S_=(_L_, ⊕, ⊗) ⊂ _U_, nazýváme zobrazení **_f<sub>|S</sub>_ : _S_ → _V_**, kde
  * _D(f<sub>|S</sub>)_ = _L_ ∩ _D(f)_
  * _f<sub>|S</sub>(u)_ = _f(u)_ pro každé _u_ ∈ _D(f<sub>|S</sub>)_
* zúžením lineráního zobrazení na podprostor _S_, toto zúžení je znovu lineárním zobrazením
