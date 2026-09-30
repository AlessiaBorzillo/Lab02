import csv
def carica_da_file(file_path):
    """Carica le foto dal file, creando un nuovo anno ogni volta che compare per la prima volta"""
    # TODO
    album = {} #creiamo il dizionario vuoto
    try:
        with open(file_path, "r") as f:
            f.readline() #salto intestazione
            reader = csv.reader(f)
            for riga in reader:
                if not riga or len(riga) < 5:
                    continue #salta la riga se è vuota o non ha tutti e 5 i campi
                codice = riga[0]
                titolo = riga[1]
                autore = riga[2]
                mese = int(riga[3])
                anno = int(riga[4])

                foto = {
                    'codice' : codice,
                    'titolo' : titolo,
                    'autore': autore,
                    'mese' : mese,
                    'anno' : anno
                }
                if anno not in album:
                    album[anno] = []
                album[anno].append(foto)
        return album
    except FileNotFoundError:
        return None


def aggiungi_foto(album, codice, titolo, autore, mese, anno, file_path):
    """Aggiunge una foto all'album, creando l'anno al volo se non è ancora presente"""
    # TODO
    if mese < 1 or mese > 12:
        return None
    for lista_foto in album.values():
        for foto in lista_foto:
            if foto['codice'] == codice:
                return None
    try:
        with open(file_path, "a") as f: #w = cancella l'intero contenuto del file csv e ci scrive dentro solo la nuova foto con  a= aggiungo in coda, mantiene cio che c'era prima
            f.write(f"{codice},{titolo},{autore},{mese},{anno}\n")
    except FileNotFoundError:
        return None
    foto = {
        'codice': codice,
        'titolo': titolo,
        'autore': autore,
        'mese': mese,
        'anno': anno
    }
    if anno not in album:
        album[anno] = []

    album[anno].append(foto)
    return foto

def cerca_foto(album, codice):
    """Cerca una foto nell'album dato il codice"""
    # TODO
    #abbiamo un dizionario dove le chiavi sono gli anni e i valori sono le liste di foto: {2021: [foto1, foto2],2022:[foto3]..}
    for lista_foto in album.values():
        for foto in lista_foto:
            if foto['codice']== codice:
                return f"{foto['codice'],foto['titolo'], foto['autore'], foto['mese'], foto['anno']}" #l'ho trovata e mi restituisce il dizionario della foto
    return None #fuori da entrambi i cicli perche altrimenti se la prima foto della lista non ha il codice cercato,l'istruzione
# 'else : return none' viene eseguita immediatamente e la funzione termina subito restituendo none, senza neanche controllare le altre foto


def elenco_foto_anno_per_titolo(album, anno):
    """Ordina i titoli delle foto di un dato anno in ordine alfabetico"""
    # TODO
    if anno not in album:
        return None
    #ora raccolgo i titoli delle foto in quel determinato anno
    titoli= []
    for foto in album[anno]:
        titoli.append(foto['titolo'])
    return sorted(titoli)


def main():
    album = []
    file_path = "album_fotografico.csv"

    while True:
        print("\n--- MENU ALBUM FOTOGRAFICO ---")
        print("1. Carica album da file")
        print("2. Aggiungi una nuova foto")
        print("3. Cerca una foto per codice")
        print("4. Elenco foto di un anno (ordinato per titolo)")
        print("5. Esci")

        scelta = input("Scegli un'opzione >> ").strip()

        if scelta == "1":
            while True:
                file_path = input("Inserisci il path del file da caricare: ").strip()
                album = carica_da_file(file_path)
                if album is not None:
                    break

        elif scelta == "2":
            if not album:
                print("Prima carica l'album da file.")
                continue

            codice = input("Codice della foto: ").strip()
            titolo = input("Titolo: ").strip()
            autore = input("Autore: ").strip()
            try:
                mese = int(input("Mese (1-12): ").strip())
                anno = int(input("Anno: ").strip())
            except ValueError:
                print("Errore: inserire valori numerici validi per mese e anno.")
                continue

            foto = aggiungi_foto(album, codice, titolo, autore, mese, anno, file_path)
            if foto:
                print(f"Foto aggiunta con successo!")
            else:
                print("Non è stato possibile aggiungere la foto.")

        elif scelta == "3":
            if not album:
                print("L'album è vuoto.")
                continue

            codice = input("Inserisci il codice della foto da cercare: ").strip()
            risultato = cerca_foto(album, codice)
            if risultato:
                print(f"Foto trovata: {risultato}")
            else:
                print("Foto non trovata.")

        elif scelta == "4":
            if not album:
                print("L'album è vuoto.")
                continue

            try:
                anno = int(input("Inserisci l'anno da consultare: ").strip())
            except ValueError:
                print("Errore: inserire un valore numerico valido.")
                continue

            titoli = elenco_foto_anno_per_titolo(album, anno)
            if titoli is not None:
                print(f'\nFoto del {anno}:')
                print("\n".join([f"- {titolo}" for titolo in titoli]))
            else:
                print(f"Nessuna foto trovata per l'anno {anno}.")

        elif scelta == "5":
            print("Uscita dal programma...")
            break
        else:
            print("Opzione non valida. Riprova.")


if __name__ == "__main__":
    main()
