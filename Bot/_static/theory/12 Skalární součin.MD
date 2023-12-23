# Skalární součin

* Zdroje:
  * [RNDr. Zdeněk Kalousek CSc.](https://kma.fp.tul.cz/?view=article&id=600&catid=147)
    * 10\. přednáška z lineární algebry: Skalární součin, Ortogonalita

## Skalární součin

* Je-li _V_=(_M_, ⊕, ⊗) vektorový prostor nad tělesem _T_ a je definováno zobrazení _M_ x _M_ → _T_ (značíme ⟨ ⋅ | ⋅ ⟩) s těmito vlastnostmi: ||(pro ∀ _u_, _v_, _w_ ∈ _M_; ∀ _α_ ∈ _T_)||
  1. ⟨_u_|_v_ ⊕ _w_⟩ = ⟨_u_|_v_⟩ + ⟨_u_|_w_⟩
  2. ⟨_u_|_α_ ⊗ _v_⟩ = _α_ ⋅ ⟨_u_|_v_⟩
  3. ⟨_u_|_v_⟩ = ⟨_v_|_u_⟩
     * Platí v reálných prostorech, v komplexních je prohození komplexně sdružené
  4. ⟨_u_|_u_⟩ ≥ 0
     * ⟨_u_|_u_⟩ = 0 ⟺ _u_ = _o_
* nazveme hodnotu ⟨_u_|_v_⟩ skalární součin vektorů _u_ a _v_ a prostor _V_ nazveme unitární prostor (prostor se skalárním součinem)
* V komplexních prostorech je skalární součin závislý na pořadí vektorů
* Na prostorech _n_-tic čísel můžeme zavést skalární součin nejjednodušeji jako

$$$render
\langle u|v\rangle=\sum_{j=1}^n\bar{u}_jv_j
$$

## Metrická matice

* Na prostoru _T<sup>n</sup>_ se dá skalární součin zavést i jinak:
* V unitárním prostoru _U_ nad _T_ vybereme _n_-tici lineárně nezávislých vektorů _g<sub>1</sub>_, _g<sub>2</sub>_, ..., _g<sub>n</sub>_ a vytvoříme matici _G_ s prvky _g<sub>ij</sub>_ = ⟨_g<sub>i</sub>_|_g<sub>j</sub>_⟩
* Pak definujeme skalární součin s metrikou _G_ jako

$$$render
\langle u|v\rangle_G=\sum_{i=1}^n\bar{u}_i(Gv)_i
$$

* ⟨_u_|_v_⟩<sub>G</sub> je skalárním součinem ⟨ lineární kombinace vektorů _g<sub>i</sub>_ s koeficienty _u<sub>i</sub>_ | lineární kombinace vektorů _g<sub>j</sub>_ s koeficienty _v<sub>j</sub>_ ⟩
* Pokud bude _G_={_g<sub>1</sub>_, _g<sub>2</sub>_, ..., _g<sub>n</sub>_} baze nějakého _n_-dimenzionálního unitárního prostoru, budou koeficienty _u<sub>i</sub>_ souřadnicemi nějakého vektoru _ũ_ v bazi _G_ a ⟨_ũ_|_ṽ_⟩ = ⟨_ũ<sup>G</sup>_|_ṽ<sup>G</sup>_⟩<sub>G</sub>

## Norma vektoru

* Na unitárním vektorovém prostoru zavádíme normu vektoru _u_ jako

$$$render
\|u\|=\sqrt{\langle u|u\rangle}
$$

  * \||_α_ ⊗ _u_\|| = |_α_| · \||_u_\||
  * \|⟨_u_|_v_⟩| ≤ \||_u_\|| · \||_v_\|| ←(Schwartzova nerovnost)
  * \||_u_ ⊕ _v_\||<sup>2</sup> = (\||_u_\|| + \||_v_\||)<sup>2</sup>

## Ortogonalita

* V unitárním vektorovém prostoru řekneme, že množina _A_={_a<sub>j</sub>_}<sub>j≥1</sub> (může být i nekonečná) je ortogonální, pokud pro každé její dva různé vektory _a<sub>i</sub>_ ≠ _a<sub>j</sub>_ je ⟨_a<sub>i</sub>_|_a<sub>j</sub>_⟩ = 0
* Podle definice je nulový vektor ortogonální ke všem vektorům, obvykle ho do ortogonálních množin ale nezařazujeme

### Ortonormalita

* Nulový vektor se dá vyřadit pomocí požadavku, kdy řekneme, že množina _A_={_a<sub>j</sub>_}<sub>j≥1</sub> je ortonormální, pokud pro každé dva její vektory je ⟨_a<sub>i</sub>_|_a<sub>j</sub>_⟩ = _δ<sub>ij</sub>_ (Kroneckerovo delta)
  * 1 při _i_ = _j_
  * 0 při _i_ ≠ _j_
  * Všechny vektory ortonormální množiny mají tedy jednotkovou velikost

### Ortogonální vektory

* Každá ortogonální množina v unitárním prostoru, která neobsahuje nulový vektor, je lineárně nezávislá
* Ortogonální množiny v unitárních prostorech jsou vhodnými kandidáty na baze těchto vektorových prostorů

### Gramův-Schmidtův algoritmus – ortogonalizace

* Jeden nenulový vektor generuje vždy ortogonální množinu
* Chceme vytvořit ortogonální bazi lineárního obalu množiny vektorů _G_
* Předpokládejme, že jsme s použitím prvních několika vektorů z _G_ vytvořili _n_-prvkovou ortogonální množinu _F<sub>n</sub>_
* Vezmeme ještě nepoužitý vektor _g_ ∈ _G_ a pokusíme se vytvořit lineární kombinaci vektoru _g_ a vektorů z množiny _F<sub>n</sub>_ tak, aby byla ortogonální ke všem vektorům z _F<sub>n</sub>_

$$$render
\tilde{f}_{n+1}&=g\bigoplus_{j=1}^n(\beta_j\otimes f_j)\\
0&=\langle f_i|\tilde{f}_{n+1}\rangle\\
0&=\langle f_i|g\bigoplus_{j=1}^n(\beta_j\otimes f_j)\rangle\\
0&=\langle f_i|g\rangle+\sum_{j=1}^n\langle f_i|\beta_j\otimes f_j\rangle\\
0&=\langle f_i|g\rangle+\sum_{j=1}^n\beta_j\langle f_i|f_j\rangle\\
$$

* V součtu na pravé straně jsou všechny skalární součiny ⟨_f<sub>i</sub>_|_f<sub>j</sub>_⟩ nulové s výjimkou toho, kde _j_ = _i_

$$$render
0&=\langle f_i|g\rangle+\beta_i\langle f_i|f_i\rangle\\
0&=\langle f_i|g\rangle+\beta_i\|f_i\|^2\\
\beta_i&=-\frac{\langle f_i|g\rangle}{\|f_i\|^2}\\
\tilde{f}_{n+1}&=g\bigoplus_{j=1}^n\left(-\frac{\langle f_j|g\rangle}{\|f_j\|^2}\otimes f_j\right)
$$
