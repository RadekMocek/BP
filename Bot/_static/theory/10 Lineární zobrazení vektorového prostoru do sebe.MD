# Lineárnı́ zobrazenı́ vektorového prostoru do sebe

## Lineární zobrazení vektorového prostoru do sebe

* Pokud _U_=(_M_, ⊕, ⊗) je vektorový prostor, můžeme uvažovat i o zobrazeních z množiny _M_ znovu do množiny _M_
  * _f_ : _U_ → _U_
  * Nazýváme (lineární) zobrazení vektorového prostoru do sebe nebo také (lineární) endomorfismus na prostoru _U_
* Endomorfismy nám umožňují aplikovat zobrazení opakovaně _f(f( ))_ a můžeme porovnávat jejich vzory a obrazy přímo pomocí vektorových operací ⊕, ⊗
  * Můžeme si klást otázku, jaké musí být vektory _u_, _b_ a číslo _λ_, aby _f(u)_ = _λ_ ⊗ _u_ ⊕ _b_

$$$render
f(u)&=\lambda\otimes u\oplus b\\
f(u)\oplus(-\lambda\otimes u)&=b\\
f(u)\oplus(-\lambda\otimes i(u))&=b\\
(f\oplus(-\lambda\otimes i))(u)&=b\\
f_\lambda(u)&=b
$$

## Vlastní vektory a vlastní čísla

* Je-li _f_ lineární endomorfismus na _U_=(_M_, ⊕, ⊗) nad tělesem _T_, pak řekneme, že _u_ je vlastní vektor zobrazení _f_, pokud _u_ ≠ _o_ a existuje _λ_ ∈ _T_ taková, že _f(u)_ = _λ_ ⊗ _u_
  * "Vlastní vektor zobrazení _f_ je takový nenulový vektor, který se zobrazí na svůj násobek"
  * _λ_ je pak vlastní číslo (vlastní hodnota) zobrazení _f_
  * Vlastní čísla pro různé vlastní vektory (stejného) lineárního endomorfismu mohou být různá
  * Nulový vektor se za vlastní nepovažuje, skalár nula ale **může** být vlastním číslem
* Množina vlastních vektorů s odlišnými vlastními čísly je lineárně nezávislá
  * Nezávislá zůstane i po přidání hlavních vektorů

## Hlavní vektory

* Je-li _f_ lineární endomorfismus na _U_=(_M_, ⊕, ⊗) nad tělesem _T_ s vlastním číslem _λ_ a vlastním vektorem _u<sup>(0)</sup>_, nazveme hlavním vektorem zobrazení _f_ řádu _k_ vektor _u<sup>(k)</sup>_ takový, že **_f_(_u<sup>(k)</sup>_) = _λ_ ⊗ _u<sup>(k)</sup>_ ⊕ _u<sup>(k-1)</sup>_**
  * (Hlavní vektor 1. řádu _u<sup>(1)</sup>_ se zobrazí na součet svého násobku s vlastním vektorem _u<sup>(0)</sup>_)

## Vlastní podprostor

* Všechny vlastní vektory lineárního endomorfismu _f_ : _U_ → _U_ se společným vlastním číslem _λ_, doplněné o nulový vektor, tvoří podprostor v _U_
  * Ten nazýváme vlastní podprostor zobrazení _f_ s vlastním číslem _λ_

## Vlastní vektory a čísla matic

* Vztah _f(u)_ = _λ_ ⊗ _u_ je ekvivalentní vztahu pro souřadnice _F<sub>E→E</sub>_ ⋅ _u<sup>E</sup>_ = _λ_ ⋅ _u<sup>E</sup>_
* Zobrazení _f<sub>λ</sub>_ je reprezentováno maticí _F<sub>λ</sub>_ = _F_ - _λ_ ⋅ _E_ (_E_ = jednotková matice), tato matice nemá plnou hodnost

## Opakované skládání

* Endomorfismy (ne nutně lineární) můžeme skládat samy se sebou
  * Vytvořená zobrazení nazýváme _n_-tými mocninami zobrazení _f_
  * **_f <sup>0</sup>_ = _i_ (identita)**
  * **_f <sup>n</sup>_ = _f(f <sup>n-1</sup>)_** pro každé _n_ ∈ ℤ
  * _f <sup>m</sup>(f <sup>n</sup>)_ = _f <sup>m+n</sup>_
  * _(f <sup>m</sup>)<sup>n</sup>_ = _f <sup>mn</sup>_
  * _f <sup>-n</sup>_ = _(f <sup>-1</sup>)<sup>n</sup>_
* Složené zobrazení se reprezentuje součinem matic, mocnina zobrazení je proto reprezentována mocninou matice _f <sup>n</sup>_ = (_F<sub>E→E</sub>_)<sup>n</sup>
* Má-li _f_ vlastní vektor _u_ s vlastním číslem _λ_, pak _f <sup>n</sup>_ má stejný vlastní vektor _u_ s vlastním číslem _λ<sup>n</sup>_

### Lineární kombinace mocnin

* Pro endomorfismus na _U_=(_M_, ⊕, ⊗) nad _T_ a mnohočlen

$$$render
P_n(x)=\sum_{k=0}^na_kx^k
$$

s koeficienty z tělesa _T_ definujeme mnohočlen _P<sub>n</sub>_ ze zobrazení _f_ jako zobrazení:

$$$render
P_n(f)=\bigoplus_{k=0}^n(a_k\otimes f^k)
$$

* Pro matice

$$$render
p_n(f)=\sum_{k=0}^na_k(F_{E\to E})^k
$$

  * Násobení matic, které vznikly jako mnohočlen z téže matice, je komutativní
* Má-li _f_ vlastní vektor _u_ s vlastním číslem _λ_, pak _P<sub>n</sub>(f)_ má stejný vlastní vektor _u_ s vlastním číslem _P<sub>n</sub>(λ)_
