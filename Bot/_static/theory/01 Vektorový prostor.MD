# Vektorový prostor

* Zdroje:
  * [RNDr. Zdeněk Kalousek CSc.](https://kma.fp.tul.cz/?view=article&id=600&catid=147)
    * 2\. přednáška z lineární algebry: Vektorový prostor, Podprostory, Příklady vektorových prostorů

## Vektorový prostor

* Definujeme vektorový prostor _V_=(_M_, ⊕, ⊗) nad tělesem _T_
  * Prvky z _M_ nazýváme vektory
  * Prvky z _T_ nazýváme skaláry
  * ⊕ je zobrazení _M_ × _M_ → _M_
  * ⊗ je zobrazení _T_ × _M_ → _M_
* Vektorový prostor (resp. dvě uvedená zobrazení) musí splňovat těchto 10 axiomů:
  * `[A1]` ***D*(⊕) = _M_ × _M_**
    * Ke každé dvojici vektorů existuje jejich součet, který je také vektorem
  * `[A2]` **_a_ ⊕ _b_ = _b_ ⊕ _a_**
    * Komutativita
    * pro ∀ (_a_, _b_) ∈ _M_ × _M_
  * `[A3]` **(_a_ ⊕ _b_) ⊕ _c_ = _a_ ⊕ (_b_ ⊕ _c_)**
    * Asociativita
    * pro ∀ (_a_, _b_, _c_) ∈ _M_ × _M_ × _M_
  * `[A4]` **_a_ ⊕ _o_ = _a_**
    * Existence nulového vektoru
    * ∃! _o_ ∈ _M_ pro ∀ _a_ ∈ _M_
  * `[A5]` **_a_ ⊕ (-_a_) = _o_**
    * Existence opačného vektoru; výsledkem je nulový vektor, nikoliv skalár nula
    * ∃ (-_a_) ∈ _M_ pro ∀ _a_ ∈ _M_
  * `[N1]` ***D*(⊗) = _T_ × _M_**
    * Ke každému číslu a vektoru existuje příslušný násobek vektoru, který je také vektorem
  * `[N2]` **1 ⊗ _a_ = _a_**
    * pro ∀ _a_ ∈ _M_
  * `[N3]` **_α_ ⊗ (_β_ ⊗ _a_) = (_α_ ⋅ _β_) ⊗ _a_**
    * pro ∀ (_α_, _β_, _a_) ∈ _T_ × _T_ × _M_
  * `[D1]` **_α_ ⊗ (_a_ ⊕ _b_) = _α_ ⊗ _a_ ⊕ _α_ ⊗ _b_**
    * pro ∀ (_α_, _a_, _b_) ∈ _T_ × _M_ × _M_
  * `[D2]` **(_α_ + _β_) ⊗ _a_ = _α_ ⊗ _a_ ⊕ _β_ ⊗ _a_**
    * pro ∀ (_α_, _β_, _a_) ∈ _T_ × _T_ × _M_
* Dále platí:
  * 0 ⊗ _a_ = _o_
  * (-1) ⊗ _a_ = (-_a_)

## Podprostor

* Je-li _V_=(_M_, ⊕, ⊗) vektorový prostor nad tělesem _T_, nazveme _U_=(_N_, ⊕, ⊗) podprostorem vektorového prostoru _V_, pokud množina _N_ ⊂ _M_ splňuje:
  * ⊕ je zobrazení _N_ x _N_ → _N_
  * ⊗ je zobrazení _T_ x _N_ → _N_
* Zapisujeme _U_ ⊂ _V_
* (Číselné těleso je automaticky společné)
* Podprostor vektorového prostoru je sám o sobě vektorovým prostorem

## Nejběžnější vektorové prostory

### Geometrické vektory

* Množiny orientovaných úseček na přímce, v rovině nebo v prostoru

### Aritmetické vektory

* _Tⁿ_ – množina _n_-tic čísel z tělesa _T_ (např. ℝ²)
* (_a₁_, _a₂_, ..., _aₙ_) ⊕ (_b₁_, _b₂_, ..., _bₙ_) = (_a₁_ + _b₁_, _a₂_ + _b₂_, ..., _aₙ_ + _bₙ_)
* _α_ ⊗ (_a₁_, _a₂_, ..., _aₙ_) = (_α_ ⋅ _a₁_, _α_ ⋅ _a₂_, ..., _α_ ⋅ _aₙ_)

### Mnohočleny jedné proměnné

* Jako mnohočleny jedné proměnné definujeme zobrazení, které každému _x_ přiřazují hodnotu:

$$$render
P(x)=a_nx^n+a_{n-1}x^{n-1}+\dots+a_1x^1+a_0x^0=\sum_{k=0}^na_kx^k
$$

  * Nejvyšší hodnota _k_, pro kterou _aₖ_ ≠ 0, označujeme jako stupeň mnohočlenu
  * (Každý mnohočlen stupně _k_ > 0 má nejvýše _k_ různých komplexních kořenů)
* _Pₙ_ – množina mnohočlenů jedné proměnné nejvýše _n_-tého stupně s koeficienty z tělesa _T_
* (_P_ ⊕ _Q_)(_x_) = (_aₙ + bₙ_) _xⁿ_ + (_aₙ₋₁ + bₙ₋₁_) _xⁿ⁻¹_ + ... + (_a₁ + b₁_) _x_ + (_a₀ + b₀_)
  * _P(x)_ = _aₙ xⁿ_ + _aₙ₋₁ xⁿ⁻¹_ + ... + _a₁ x_ + _a₀_
  * _Q(x)_ = _bₙ xⁿ_ + _bₙ₋₁ xⁿ⁻¹_ + ... + _b₁ x_ + _b₀_
* (_α_ ⊗ _P_)(_x_) = (_α_ ⋅ _aₙ_) _xⁿ_ + (_α_ ⋅ _aₙ₋₁_) _xⁿ⁻¹_ + ... + (_α_ ⋅ _a₁_) _x_ + (_α_ ⋅ _a₀_)
* Omezení stupně není nutné

### Mnohočleny dvou proměnných

$$$render
P(x,y)=\sum_{j=1}^m\sum_{k=1}^na_{j,k}x^jy^k
$$

  * Stupněm takového mnohočlenu je nejvyšší hodnota součtu _j_+_k_, pro kterou existuje nenulové _a<sub>j,k</sub>_
* Zavedením sčítání a násobení číslem podobně jako u mnohočlenů jedné proměnné získáme opět vektorový prostor (omezení stupně opět není nutné)

### Lineární mnohočleny více proměnných

* Mnohočlen více proměnných nejvýše prvního stupně (také nazýváno lineární funkce více proměnných)

$$$render
L(x_1,x_2,\dots,x_n)=a_1x_1+a_2x_2+\dots+a_nx_n+a_0=a_0+\sum_{k=1}^na_kx_k
$$

* Zavedení sčítání a násobení číslem opět podobné jako u mnohočlenů jedné proměnné
* Počet proměnných pro lineární funkce je pevný

### Funkční prostory

* Množina všech funkcí se stejným definičním oborem a hodnotami ze stejného tělesa tvoří vektorový prostor
* (_f_ ⊕ _g_)(_x_) = _f(x)_ + _g(x)_
* (_α_ ⊗ _f_)(_x_) = _α_ ⋅ _f(x)_

### Omezené funkce

* Omezená funkce _f_ je funkce taková, že existuje číslo _c<sub>f</sub>_ takové, že |_f(x)_| ≤ _c<sub>f</sub>_
* |(_f_ ⊕ _g_)(_x_)| ≤ _c<sub>f</sub>_ + _c<sub>g</sub>_

### Kladné funkce

* _f(x)_ > 0
* Při běžném zavedení operací není vektorovým prostorem (absence nulového a opačného prvku)
* Můžeme ale zavést operace jako:
  * (_f_ ⊕ _g_)(_x_) = _f(x)_ ⋅ _g(x)_
  * (_α_ ⊗ _f_)(_x_) = \[_f(x)_\]_ᵅ_

### Rovnice

* Rovnice _f(x)_ = _b_
  * tvoří-li možné funkce na levé straně vektorový prostor s "přirozeně" zavedeným sčítáním a násobením, můžeme tyto operace zavést i pro celé rovnice
* _R_ : _f(x)_ = _a_
* _S_ : _g(x)_ = _b_
* _R_ ⊕ _S_ = rovnice _f(x)_ ⊕ _g(x)_ = _a_ + _b_
* _α_ ⊗ _R_ = rovnice _α_ ⊗ _f(x)_ = _α_ ⋅ _a_
