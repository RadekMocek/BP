# Lineárnı́ kombinace vektorů

* Zdroje:
  * [RNDr. Zdeněk Kalousek CSc.](https://kma.fp.tul.cz/?view=article&id=600&catid=147)
    * 1\. přednáška z lineární algebry: Gaussova eliminační metoda
    * 2\. přednáška z lineární algebry: Lineární kombinace vektorů
    * 3\. přednáška z lineární algebry: Lineární obal množiny

## Lineární kombinace vektorů

_b_ = _α<sub>1</sub>_ ⊗ _a<sub>1</sub>_ ⊕ _α<sub>2</sub>_ ⊗ _a<sub>2</sub>_ ⊕ · · · ⊕ _α<sub>n</sub>_ ⊗ _a<sub>n</sub>_

* Vektor _b_ je lineární kombinací vektorů _a<sub>1</sub>_, _a<sub>2</sub>_, . . . , _a<sub>n</sub>_ s koeficienty _α<sub>1</sub>_, _α<sub>2</sub>_, . . . , _α<sub>n</sub>_ → je součtem jejich násobků
* Pro _V_=(_M_, ⊕, ⊗) nad _T_, kde _a_ ∈ _M_, _α_ ∈ _T_

## Lineární obal množiny vektorů

* Je-li _A_ = {_a<sub>1</sub>_, _a<sub>2</sub>_, ..., _a<sub>n</sub>_(, ...)} množina vektorů z _M_ a _V_=(_M_, ⊕, ⊗) vektorový prostor nad tělesem _T_, nazveme množinu všech lineárních kombinací vektorů _a<sub>i</sub>_ **lineárním obalem** množiny _A_. Lineární obal množiny _A_ značíme span(_A_)

1. Pokud vynásobíme vektor z množiny _A_ nenulovým číslem, span(_A_) se nezmění (lineární obal množiny _A_ zůstane stejný)
2. Obal se také nezmění, pokud k jednomu vektoru přičteme libovolný násobek **jiného** vektoru
3. Obal se také nezmění, pokud vynecháme vektor, který je lineární kombinací **ostatních** vektorů (takový vektor můžeme také přidat)

* Je-li _A_ = {_a<sub>1</sub>_, _a<sub>2</sub>_, ..., _a<sub>n</sub>_, ...} množina vektorů z _M_ a _V_=(_M_, ⊕, ⊗) vektorový prostor nad tělesem _T_, pak trojice (span(_A_), ⊕, ⊗) je **podprostorem** ve _V_
  * Říkáme, že množina _A_ generuje podprostor (span(_A_), ⊕, ⊗)

## Gaussova eliminační metoda

* Z každé matice lze vytvořit nějakou matici v horním stupňovitém tvaru pomocí posloupnosti gaussovských operací:

1. Výměna řádků
2. Nenulové vynásobení řádku
3. Přičtení násobku jiného řádku

* Gaussova eliminační metoda spočívá v opakování postupu, kdy se v aktuálně zpracovávané submatici snažíme pomocí gaussovských operací vytvořit v prvním sloupci nuly na všech místech nejvýše s výjimkou prvního řádku submatice
