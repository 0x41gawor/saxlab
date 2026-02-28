# 26-02-22

![image-20260222120359290](C:\Users\41gaw\AppData\Roaming\Typora\typora-user-images\image-20260222120359290.png)

![image-20260222120817323](C:\Users\41gaw\AppData\Roaming\Typora\typora-user-images\image-20260222120817323.png)

![image-20260222121548235](C:\Users\41gaw\AppData\Roaming\Typora\typora-user-images\image-20260222121548235.png)

## Ćwiczenia

### [Get Your Sax Together - 3 Saxophone Breathing Exercises You MUST Know"](https://youtu.be/MijjNM3Wwuo?si=FBarY_8_OTUZbrJb)

![image-20260222123405024](C:\Users\41gaw\AppData\Roaming\Typora\typora-user-images\image-20260222123405024.png)

Tutaj chłop robi Demo.

# Ćwiczenia na weeks 1/2

## 1B.01 Ćwiczenie "Ssss"

Instrukcje:

Przygotowania

Pętla:

1. Wdech nosem (4 sekundy)
2. Wydech na "ssss" (8-12 sekund)

Definicja sesji: 10 powtórzeń pętli

## 1B.02 Tactical Happy Breath

Przygotowanie:

- Stań prosto z dobrą posturą
- Prawa ręka na belly, lewa na klatkę
- Relax :)
- Ustaw metronom na `X \in {50, 90} [bpm]`

Pętla:

- 4 counts In: Pełny wdech nosem napełnij chest i belly
- 4 counts Hold: Bez napinania trzymaj powietrze
- 6 counts Shh: Firmly exhale with "Sh" throught your teeths (zobacz [demo](https://youtu.be/MijjNM3Wwuo?si=4ehkei3lhu9l2wZA&t=264))

Definicja sesji: 2-3 minuty czegoś takiego ciągiem z gradually slowing down the bpms

## 1A.01 Sam ustnik bez feedback

1. Załóż reed (pl. stroik)
2. Ułóż dolną wargę lekko zawinietą na zęby
3. Górne zęby stabilnie na ustniku
4. Stały strumień powietrza (nie dmuchnięcie)

Sesja: do znudzenia, ok 10-15 min

Tu ćwiczysz tzw. [Embochure](https://en.wikipedia.org/wiki/Embouchure) - [Better Sax - "Copy this sax embochure for a Beatiful sound"](https://youtu.be/YxUJYNttd0A?si=dAvcf9VFXKeV9glI)

## 1A.02 Sam ustnik z feedback stabilności

1. Załóż reed (pl. stroik)
2. Ułóż dolną wargę lekko zawinietą na zęby
3. Górne zęby stabilnie na ustniku
4. Otwórz apki typu "sound meter" żeby kontrolować stabilność (variability decybeli)
5. Stały strumień powietrza (nie dmuchnięcie)

Definicja sesji: do znudzenia, ok 10-15 min

Tu ćwiczysz tzw. [Embochure](https://en.wikipedia.org/wiki/Embouchure) - [Better Sax - "Copy this sax embochure for a Beatiful sound"](https://youtu.be/YxUJYNttd0A?si=dAvcf9VFXKeV9glI)

## 1A.03 Nuta B (polskie H) bez feedback

1. Ustaw lewy kciuk na B

Definicja sesji: 5 sekund dźwięku, 5 sekund przerwy, 10 powtórzeń

Tu ćwiczysz kontrolę powietrza oraz uzyskanie czystego tonu.

## 1A.04 Nuta B z feedback

Instrukcje:

1. Ustaw lewy kciuk na B
2. Odpal apkę typu tuner

Definicja sesji: 5 sekund dźwięku, 5 sekund przerwy, 10 powtórzeń

Tu ćwiczysz kontrolę powietrza oraz uzyskanie czystego tonu.

# Plan trenigowy 1stage

## Dzień 1

- 3x 1B.01 ("Ssss") [8s wydech] 2-3min break
- 2 x 1B.02 (Tactical Happy Breath)

> Nie unoś barków
>
> Nie napinaj szyi

## Dzień 2

- 4x 1B.01 ("Ssss") [12s wydech] 2-3min break
- 2 x 1B.02 (Tactical Happy Breath) 2-3min break

## Dzień 3

- 3x 1B.01 ("Ssss") [12s wydech] 2-3min break
- 3x 1B.02 (Tactical Happy Breath) 2-3min break

> W 1B.01 spróbuj:
>
> - pierwsze 4 sekundy cicho
> - kolejne 4 sekundy minimalnie głośniej
> - ostatnie 4 sekundy znowu ciszej

Ten dzień powtarzać do skutku.

## Dzień 4

- 2 x 1B.01 "Ssss" [12s wydech]
- 1 x 1A.01 Sam ustnik bez feedback
- 1 x 1A.02 Sam ustnik z feedback stabilności

> Cel ustnik brak piszczenia

## Dzień 5

- 2 x 1B.01 "Ssss"
- 1 x 1A.01 Sam ustnik bez feedback
- 1 x 1A.02 Sam ustnik z feedback stabilności

> Powstarzane aż do spełnienia warunków:
>
> - 8–10 sekund czystego tonu
>
> - brak pisków
>
> - brak napięcia szyi

## Dzień 6

- 1x 1B.01 "Ssss"
- 1 x 1A.01 Sam ustnik bez feedback
- 2 x 1A.03 Nuta B (polskie H) bez feedback

> To powtarzasz aż B brzmi czysto.

## Dzień 7

- 1x 1B.01  "Ssss"
- 1 x 1A.01  Sam ustnik bez feedback
- 1 x 1A.03  Nuta B (polskie H) bez feedback
- 1 x 1A.04  Nuta B z feedback

## Milestone - Kryterium przejścia do BAGAB

Nie kalendarz.
Warunek jakościowy:

- 12 sekund stabilnego „ssss”
- 8–10 sekund stabilnego tonu z ustnika
- 5 sekund czystej B bez pisku (10 powtórzeń)

 # 26-02-28 `saxlab.py`

Napisałem sobie skrypt, do benchmarkowania moich prób.

Skrypt nagrywa mikorofon 10 sekund i potem daje statystyki.

```sh
SAXLAB RESULTS

Mean frequency: 594.05 Hz
Std frequency: 8.59 Hz
Pitch stability: 24.41 cents

Mean dB (RMS): -46.83
Std dB (RMS): 3.03

Stable tone duration: 8.52 sec
```

Typowa **częstotliwość** usnitka safonu to ~587Hz

![image-20260228142902023](C:\Users\41gaw\AppData\Roaming\Typora\typora-user-images\image-20260228142902023.png)