# ZPRP-METEO-MODEL

<a target="_blank" href="https://cookiecutter-data-science.drivendata.org/">
    <img src="https://img.shields.io/badge/CCDS-Project%20template-328F97?logo=cookiecutter" />
</a>

Projekt badawczy mający na celu opracowanie modelu do przewidywania wartości meteorologicznych, takich jak temperatura, ciśnienie i opady. Prognozy będą wizualizowane na prostych wykresach liniowych w dedykowanej aplikacji.

---

## **Opis**

Projekt obejmuje:
- Przegląd literatury naukowej w celu wybrania najlepszych metod.
- Eksperymenty z różnymi architekturami sieci neuronowych, aby wytrenować najdokładniejszy model prognostyczny.
- Wizualizację wyników modelu w oparciu o dane aktualne i historyczne.

Projekt jest inspirowany artykułem [Springer](https://link.springer.com/article/10.1007/s00500-020-04954-0#Sec16), jednak wprowadza zmiany, takie jak:
- Wykorzystanie innego źródła danych: [Meteostat](https://dev.meteostat.net/guide.html).
- Proste zastosowanie modelu na bieżących danych meteorologicznych.

---

## **Kluczowe funkcjonalności**

- **Reprodukcja eksperymentów**: Kod projektu umożliwia odtworzenie eksperymentów przeprowadzonych podczas prac badawczych.  
- **Wizualizacja prognoz**: Prosta aplikacja Streamlit prezentuje:
  - Prognozy temperatury.
  - Przewidywania ciśnienia.
  - Szacowania opadów.

---

## **Instalacja**

Aby uruchomić projekt lokalnie:

1. Sklonuj repozytorium:
   ```bash
   git clone https://gitlab-stud.elka.pw.edu.pl/mostasze/zprp-meteo-model.git
   cd zprp-meteo-model
   ```

2. Utwórz i aktywuj środowisko wirtualne
    ```bash
    make create_environment
    ```

3. Zainstaluj zależności:
    ```bash
    make requirements
    ```

---

## **Sposób użycia**

1. Przgotowanie klucza do Meteostat API
   - Należy zasubskrybować jeden z [planów meteostat](https://rapidapi.com/meteostat/api/meteostat/pricing)
   - Następnie należy wejść na [RapidApi meteostat](https://rapidapi.com/meteostat/api/meteostat/playground/) i skopiować **x-rapidapi-key**
   - Skopiowany klucz należy wkleić do pliku .env w katalogu głównym projektu.

2. Przygotowanie danych:
    ```bash 
    make prepare_data
    ```

3. Uruchomienie eksperymentów:
    ```bash
    make run_experiments
    ```

---

## Organizacja projektu

```
├── LICENSE            <- Licencja Open-Source
├── Makefile           <- Makefile z komendami
├── README.md          <- README 
├── data
│   ├── normalized     <- Znormalizowane dane
│   ├── processed      <- Pobrane i przetworzone dane
│   └── raw            <- Oryginalne dane
│
├── docs               <- Folder z dokumentacją
│   ├── Design_Proposal.md
│   └── Analiza_Literatury.md
│
├── notebooks          <- Notatniki Jupyter. Konwencja nazywania: numer + krótki opis
│   ├── 02_exploratory_data_analysis.ipynb
│   └── 03_perform_experiment.ipynb
│
├── reports            <- Wygenerowane analizy, np. HTML, PDF
│   └── figures        <- Grafiki i wykresy użyte w raportach
│
├── requirements.txt   <- Wymagania środowiska
│
├── setup.py           <- Skrypt instalacyjny projektu
├── pyproject.toml     <- Plik konfiguracyjny projektu
│
└── zprp_meteo_model   <- Kod źródłowy projektu
    ├── data/          <- Moduły przetwarzające dane
    ├── model/         <- Kod definiujący architektury modeli
    ├── training/      <- Moduły związane z trenowaniem modeli
    └── utils/         <- Narzędzia wspomagające projekt

```

---

## **Autorzy**

- Michał Sadowski
- Mateusz Ostaszewski
- Szymon Łukawski

---

## **Licencja**

Projekt jest objęty licencją MIT. Szczegóły można znaleźć w pliku [LICENSE](LICENSE). 

---

## **Dodatkowa dokumentacja**

Szczegółowe informacje o projekcie znajdują się w dodatkowych plikach:  
- [Design Proposal](docs/Design_Proposal.md)
- [Analiza literatury](docs/Analiza_Literatury.md)

--------

