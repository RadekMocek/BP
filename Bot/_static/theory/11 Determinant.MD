# Determinant

* Zdroje:
  * [RNDr. Zdeněk Kalousek CSc.](https://kma.fp.tul.cz/?view=article&id=600&catid=147)
    * Lineární algebra: Determinanty

## Determinant lineárního zobrazení

* U (lineárního) endomorfismu _f_ patří vzory i obrazy do stejné množiny, můžeme je tedy navzájem porovnávat
* Nemusíme se zabývat jednotlivými vektory, můžeme např. porovnávat vztahy mezi množinou _Ω_ a _f(Ω)_
  * _f(Ω)_ nazýváme obrazem množiny _Ω_
  * _f(Ω)_ = {_v_ = _f(u)_; _u_ ∈ _Ω_}
* Poměr velikostí množin _Ω_ a _f(Ω)_ u lineárního endomorfismu je vždy stejný pro všechny množiny _Ω_
  * Tento poměr nazýváme determinant lineárního zobrazení
  * Značíme det(_f_)
  * Pro každou množinu vektorů _Ω_ je **_μ(f(Ω))_ = det(_f_) ⋅ _μ(Ω)_**
* Determinant složeného zobrazení je součinem determinantů
  * det(_g(f)_) = det(_g_)⋅det(_f_)

## Determinant matice

* Zaveden ve čtvercových maticích
* Determinantem čtvercové matice řádu _n_ se nazývá součet všech součinů _n_ prvků této matice takových, že v žádném z uvedených součinů se nevyskytují dva prvky z téhož řádku ani z téhož sloupce (v každém součinu je každý řádek i sloupec matice zastoupen právě jedním prvkem); každý součin je navíc označen paritou permutace
* Všechny matice, které reprezentují totéž zobrazení v různých bazích, mají determinanty stejné
* |_F_| = 0 ⟺ ker(_f_) ≠ {_o_}
  * Pokud je determinant matice _F_ roven nule, pak je jádro zobrazení _f_ netriviální (nenulové) a matice je singulární

## Metody výpočtu

* K výpočtu determinantu můžeme použít GEM / Sarrusovo pravidlo / rozvoj podle řádku (sloupce)

### GEM

* Má-li matice pod diagonálou (nebo nad ní) samé nuly, je determinant matice roven součinu jejích diagonálních prvků
* |_A_ ⋅ _B_| = |_A_| ⋅ |_B_|
* Násobení gaussovskými maticemi může ovlivnit hodnotu determinantu
  * Při výměně řádků matice se mění znaménko determinantu
  * Přičtením násobku jednoho řádku k jinému řádku se determinant matice nemění
  * Pokud násobíme nějaký řádek číslem (a není to pouze s účelem přičtení tohoto násobku k jinému řádku), determinant je také vynásoben tímto číslem (při dělení vydělen) (pro zachování hodnoty determinantu původní matice je třeba provést s determinantem nové matice opačnou operaci)

### Sarrusovo pravidlo

$$$render
[a,b;c,d]\sim[a,b;0,d-\frac{c}{a}\cdot b]=a\left(d-\frac{bc}{a}\right)=ad-bc
$$

* (Od druhého řádku odečteme _c/a_-násobek prvního řádku)
* Determinant matice 3×3 lze dokázat podobně (= _aei_ + _dhc_ + _bfg_ - _ceg_ - _bdi_ - _fha_)
* Sarrusovo pravidlo je pouze mnemotechnická pomůcka, s jejíž pomocí si můžeme odvodit "základní" permutační vzorec pro výpočet determinantu, a funguje pouze na matice 2×2 a 3×3 (vánočka)

### Rozvoj podle řádku

$$$render
|A|=\sum_{j=1}^n(-1)^{i+j}\cdot a_{ij}\cdot|A_{ij}|
$$
