# Frobeniova věta pro obecná lineárnı́ zobrazenı́

* Zdroje:
  * [RNDr. Zdeněk Kalousek CSc.](https://kma.fp.tul.cz/?view=article&id=600&catid=147)
    * 6\. přednáška z lineární algebry: Frobeniova věta

## Frobeniova věta

* Je-li _f_ : _U_=(_M_, ⊕<sub>u</sub>, ⊗<sub>u</sub>) → _V_=(_N_, ⊕<sub>v</sub>, ⊗<sub>v</sub>) lineární zobrazení, pak pro řešení rovnice _f(x)_ = _b_ (pro _b_ ∈ _N_) platí:
  1. Řešení existuje, pokud _b_ ∈ _W(f)_
  2. Je-li _f(x)_ = _b_ (pro _b_ ∈ _W(f)_ a _x_ ∈ _M_), pak _f(y)_ = _b_, právě když existuje _k_ ∈ ker(_f_) takové, že _y_ = _x_ ⊕<sub>u</sub> _k_
     * _x_ a _y_ se liší o nenulový vektor _k_, jehož obraz ale nulový je (protože _k_ je součástí jádra zobrazení)
     * Pokud ker(_f_) = {_o_}, pak je lineární zobrazení _f_ prosté
* Postup řešení rovnice _f(x)_ = _b_ (hledáme vzor _x_)
  1. Najdeme jádro zobrazení _f_ a nějakou jeho bazi _K_={_k<sub>1</sub>_, _k<sub>2</sub>_, ..., _k<sub>K</sub>_}
  2. Najdeme partikulární řešení: nějaké _x<sub>p</sub>_, kde _f(x<sub>p</sub>)_ = _b_
  3. Řešení: {_x_ = _x<sub>p</sub>_ + libovolná lineární kombinace vektorů baze jádra}

$$$render
x=x_p\oplus\bigoplus_{j=1}^K\alpha_j\otimes k_j
$$

* Pro libovolnou sadu koeficientů _α_ ∈ _T_
* **dim(_D(f)_) = dim(_W(f)_) + dim(ker(_f_))**

### Souvislost s řešením soustav lineárních rovnic

* Je-li _A_ matice <i>m</i>×<i>n</i>, _b_ ∈ _T<sup>m</sup>_ a _x_ ∈ _T<sup>n</sup>_
  * Je násobení _A_ krát _x_ lineární zobrazení _T<sup>n</sup>_ → _T<sup>m</sup>_
  * Rovnice _Ax_ = _b_ je soustavou lineárních rovnic pro _n_ neznámých složek vektoru _x_
* Pokud nám řešení rovnice nevyjde jednoznačně, musíme zvolit neznámé jako parametry, pak bude výsledkem část neobsahující parametry a další část pro každý parametr
  * Kdybychom řešili homogenní rovnici (soustava s nulovou pravou stranou), dostali bychom stejný výsledek až na část neobsahující parametry
  * Část obsahující parametry je tedy jádrem soustavy a vektor bez parametrů je partikulárním řešením
