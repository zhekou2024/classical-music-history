#!/usr/bin/env python3
"""One-off generator for spotify_canonical_map.json — delete after run."""
import html as html_lib
import json
import os
import re
import subprocess
import sys

BASE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(BASE, "spotify_canonical_map.json")

ORDER = [
    "josquin", "palestrina", "lasso", "byrd", "monteverdi", "pachelbel", "vivaldi", "bach", "handel", "haydn",
    "clementi", "mozart", "beethoven", "schumann", "chopin", "liszt", "wagner", "brahms", "tchaikovsky", "faure",
    "debussy", "satie", "ravel", "schoenberg", "bartok", "stravinsky", "shostakovich", "glass",
]

# (spotify_id, canonicalPerformer, canonicalAlbum, canonicalTrackTitle)
ROWS = {
    "josquin": [
        ("2J3Mmybwue0jyQ0UVMYurH", "The Tallis Scholars; Peter Phillips", "Josquin: Missa Pange Lingua & Missa La Sol Fa Re Mi", "Josquin: Ave Maria... Virgo Serena"),
        ("403DSHmLTLhOAbziYU5K8s", "The Tallis Scholars; Peter Phillips", "Josquin: Missa Pange Lingua & Missa La Sol Fa Re Mi", "Missa Pange lingua: Kyrie"),
        ("7sG9vHVIyn67MEyNTswOGG", "The Tallis Scholars; Peter Phillips", "Josquin: Missa L'homme Armé Super Voces Musicales & Missa L'homme Armé Sexti Toni", "Josquin: Missa L'homme armé Super voces musicales: Kyrie"),
        ("4l5OgQTWOYqkmGBSBquZrq", "Collegium Vocale Gent; Philippe Herreweghe", "Josquin: Miserere mei Deus", "Miserere mei, Deus, IJ. 50: I. Miserere mei, Deus"),
        ("3ZsVslQdT0boNl4kJvCQod", "La Chapelle Royale; Philippe Herreweghe", "Josquin: Stabat Mater dolorosa", "Stabat Mater dolorosa"),
        ("58520EfhMImCjWnRscmEoE", "The Tallis Scholars; Peter Phillips", "Josquin: Missa De Beata Virgine & Missa Ave Maris Stella", "Josquin: Missa De Beata Virgine - 01. Kyrie 1"),
        ("3TT4iD2RzUUSHKFsXmzCe3", "The Tallis Scholars; Peter Phillips", "Josquin: Missa L'homme Armé Super Voces Musicales & Missa L'homme Armé Sexti Toni", "Josquin: Missa L'homme armé Sexti toni: Kyrie"),
        ("6urrE0qYScNOMPYtvOFN5b", "The Hilliard Ensemble; Paul Hillier", "Josquin: Laments, Motets and Chansons", "Des Prez: La déploration de Jehan Ockeghem \"Nymphes des bois / Requiem\""),
        ("6PgBDBmUXvjeSCqmyuFg1a", "Vox Luminis; Lionel Meunier", "Josquin des Prez: Motets", "Mille regretz"),
        ("34LintczDLOCdT5zE6lirN", "The Tallis Scholars; Peter Phillips", "Josquin: Missa Gaudeamus & Missa L'ami Baudichon", "Inviolata, integra, et casta es Maria à 5"),
    ],
    "palestrina": [
        ("1Cn5toSyPYqfupygKG6LJx", "The Tallis Scholars; Peter Phillips", "Palestrina: Missa Papae Marcelli", "Palestrina: Missa Papae Marcelli - 01. Kyrie 1"),
        ("4szYZhHxI9XnPaEXRhK8F5", "The Tallis Scholars; Peter Phillips", "Palestrina: Stabat mater & Motets", "Stabat mater"),
        ("6xzg8scb8U1jkvDFWUscPU", "Choir of New College, Oxford; Robert Quinney", "Palestrina: Motets", "Sicut cervus"),
        ("2vKI4zYtsWE5EH1c7BTSX7", "The Sixteen; Harry Christophers", "Palestrina: Song of Songs", "Song of Songs - Osculetur me osculo oris sui"),
        ("6M6GP0aCCCbaII48nQnHsS", "The Tallis Scholars; Peter Phillips", "Palestrina: Missa Brevis", "Palestrina: Missa Brevis: Kyrie"),
        ("3dbLEecTVars0hhhilbEZW", "Choir of Christchurch St Lawrence; Colin Sapsford", "Palestrina: Masses", "Missa Aeterna Christi Munera: I. Kyrie Eleison"),
        ("5h6Y8yCev2ZRLKshGe8pmi", "The Tallis Scholars; Peter Phillips", "The Tallis Scholars sing Palestrina", "Tu es Petrus - 6vv"),
        ("4yD4K74x4qOc5t0R4CIA8B", "The Tallis Scholars; Peter Phillips", "Palestrina: Missa Papae Marcelli; Missa Assumpta est Maria", "Palestrina: Missa Assumpta est Maria - 01. Kyrie 1"),
        ("2Bll7Z5cuQf5jhsGJE7IwM", "The Sixteen; Harry Christophers", "Palestrina: Song of Songs and Sacred Choral Music", "Super flumina Babylonis"),
        ("6CD5CwHZ3wHNxoWARsDsg7", "The Tallis Scholars; Peter Phillips", "The Tallis Scholars sing Palestrina", "O Magnum Mysterium"),
    ],
    "lasso": [
        ("1lKi5QLMZPCcGC8U9fkYHX", "Hilliard Ensemble; Paul Hillier; Kees Boeke Consort", "Lasso: The Seven Penitential Psalms", "Psalmi Davidis poenitentiales: Domine ne in furore tuo...miserere"),
        ("017E9shJQEnQn5mXEXyoSQ", "Cantus Cölln; Konrad Junghänel", "Lasso: Prophetiae Sibyllarum", "Prophetiae Sibyllarum: 1. Carmina Chromatico"),
        ("6bKTsXo3rSLphHFhhtt5Ti", "Concerto Italiano; Rinaldo Alessandrini", "Monteverdi / Lasso / Frescobaldi", "Ola, o che bon eccho!"),
        ("4xxRiaJQHFJ83aLVE1Xwdj", "Huelgas Ensemble; Paul Van Nevel", "Lasso: Lagrime di San Pietro", "Lagrime di San Pietro: Part I: I. Il magnanimo Pietro - Vocal"),
        ("5e7abRs313tkFJnrZwZtEs", "The Hilliard Ensemble; Paul Hillier", "Lasso: Chansons", "Matona mia cara"),
        ("4B26NQ2MmplsiTUdXqobOw", "The Hilliard Ensemble; Paul Hillier", "Lasso: Chansons", "Susanne un jour"),
        ("4jBWDr2bVsanVd1x3h7XCO", "Choir of New College, Oxford; Edward Higginbottom", "Lasso: Motets", "Tristis est anima mea"),
        ("3azguMMyZ92cvpOQxYY7f3", "The King's Singers", "Lasso: Madrigals", "Lassus: Magnum opus musicum: No. 414, In hora ultima"),
        ("5DBsYBuTFtNMBrDvmy8A0O", "Dominika Skowrońska", "Lasso: Motets", "Oculus Non Vidit"),
        ("6QvgM4IdV1EY43K749KMUX", "Netherlands Chamber Choir; Paul Van Nevel", "Lasso: Sacred Music", "Jubilate Deo"),
    ],
    "byrd": [
        ("7jjQIEvTLpstEHwSjZSren", "The Cardinall's Musick; Andrew Carwood", "Byrd: The Masses", "Mass for three voices - Edited David Skinner: 1. Kyrie"),
        ("3647Fo9uKYZkzm0aoSuER4", "The Tallis Scholars; Peter Phillips", "Byrd: The Great Service", "William Byrd - The Great Service: I. Venite"),
        ("02zsmM3jFs6hBDkfmw0bRF", "Davitt Moroney", "Byrd: My Ladye Nevells Booke", "Qui passe for my Lady Nevell: Qui Passe, \"for my ladye nevell\""),
        ("1DMBqy5BuGoImegkwIHbA6", "Choir of King's College, Cambridge; David Willcocks", "Byrd: Sacred Choral Music", "Ave verum corpus"),
        ("0wxUsUNgkRsGj6DdvT7imt", "Consort of Musicke; Anthony Rooley", "Byrd: Psalms, Sonets and Songs of Sadnes and Pietie (1588)", "Psalms, Sonets and Songs of Sadnes and Pietie (1588)"),
        ("75a7x4tV0lFSxkoWkrOqXP", "Cantores in Ecclesia", "William Byrd: Cantiones sacrae 1575", "William Byrd - Tribue, Domine (Cantiones sacrae 1575)"),
        ("64Fxq9iYytqh51yKDFwkTr", "Davitt Moroney", "Byrd: The Complete Keyboard Music", "The Bells, BK 38"),
        ("0Pon0Qi0CiOM1DO46ZyiJ8", "Elaine Thornburgh", "William Byrd: Keyboard Music", "John Come Kiss Me Now"),
        ("1RBTtgSeMIsTBnfbY40mgV", "Alamire; David Skinner", "Byrd: Consort Songs", "O God Give Ear"),
        ("3xIp6yHHTA1152Nb8QcYaX", "The Sixteen; Harry Christophers", "William Byrd: Lullabies and Consort Music", "William Byrd - Lullaby My Sweet Little Baby"),
    ],
    "monteverdi": [
        ("4Wldo68Vwtdl3NvZVWBoQD", "English Baroque Soloists; John Eliot Gardiner", "Monteverdi: L'Orfeo", "Monteverdi: L'Orfeo / Prologo - Toccata"),
        ("3UvEeeqUaMqVZnJFe9Xegh", "The English Concert; Harry Bicket", "Monteverdi: L'incoronazione di Poppea", "L'incoronazione di Poppea / Act 3: Pur ti miro"),
        ("0CQ1mvMHzsWlMg1ZfS0C4R", "Monteverdi Choir; English Baroque Soloists; John Eliot Gardiner", "Monteverdi: Vespers of the Blessed Virgin", "Performing Edition by John Eliot Gardiner: 1. Deus in adjutorium ..."),
        ("1ntmcjjoXxNH7kkPXvFpWh", "English Baroque Soloists; John Eliot Gardiner", "Monteverdi: Il combattimento di Tancredi e Clorinda", "Il Combattimento di Tancredi e Clorinda, SV 153: 1. Tancredi, che Clorinda un homo stima"),
        ("7t5fKB6BxocfxgjtzvWI0m", "Concerto Italiano; Rinaldo Alessandrini", "Monteverdi: Madrigals, Book 8", "Hor Che'l Ciel e la Terra E'l Vento Tace"),
        ("3WcomUseVZ2XRddmCPbCkO", "Concerto Italiano; Rinaldo Alessandrini", "Monteverdi: Lamento d'Arianna", "Lamento D'Arianna: I. Lasciatemi Morire"),
        ("1h2K7Din4VBkdKeZsfTfL3", "Concerto Italiano; Rinaldo Alessandrini", "Monteverdi: Madrigals, Book 8", "Lamento della ninfa, SV 163"),
        ("2mQTLLHRWBi0mbNogLEWN5", "Concerto Vocale; René Jacobs", "Monteverdi: Il ritorno d'Ulisse in patria", "Il ritorno d'Ulisse in patria: Sinfonia"),
        ("4BB4YwowXQZbFMAy5nGwQL", "Il Nuove Musiche; Krijn Koetsveld", "Monteverdi: Madrigals, Book 5", "Madrigals, Book 5, SV 94–106: Cruda amarilli, SV 94"),
        ("0phz2mcJbTzJOHba6NeW2U", "Ensemble Vocal Michel Corboz", "Monteverdi: Selva morale e spirituale", "Claudio Monteverdi - Dixit Dominus (Secondo), SV 264"),
    ],
    "pachelbel": [
        ("7GKxgcNQeTDY8CM9LWAlzQ", "Herbert von Karajan; Berliner Philharmoniker", "Karajan / Pachelbel", "Canon in D Major, P. 37/1 (Orch. Seiffert) - Recorded 1969"),
        ("2XgqyX4cUKh1cWEswUmo8a", "Michael Schneider; Orchester der J. S. Bach-Stiftung", "Pachelbel: Organ Works", "Pachelbel: Chaconne in F Minor"),
        ("1aYXqqqxdoxUrXNVdBZNdt", "Antoine Bouchard", "Pachelbel: Organ Works", "Chorale Prelude \"Dies sind die heil'gen zehn Gebot\" - POP 39"),
        ("6DQUzNlaiv9BZwpphr0a2Z", "Michael Schneider; Orchester der J. S. Bach-Stiftung", "Pachelbel: Organ Works", "Hexachordum Apollinis: Aria prima"),
        ("4Y5rMkNyznXCji4vSI9ugU", "Musica Alta Ripa", "Pachelbel: Partitas for Two Violins", "Partie (Suite) in C Major for 2 Violins and Basso Continuo: I. Sonatina"),
        ("18mhHyy5bcNMAzM2eH83ho", "Michael Schneider", "Pachelbel: Organ Works", "Toccata in E Minor"),
        ("6TgkZUYukw0HNYSn5kyhbM", "Michael Schneider; Orchester der J. S. Bach-Stiftung", "Pachelbel: Organ Works", "Ciaccona in D Minor (POP 14): Ciacona in D Minor"),
        ("2dD2y2UEtIAPp6x2ItqtPy", "Michael Schneider; Orchester der J. S. Bach-Stiftung", "Pachelbel: Organ Works", "Magnificat-Fugue No. 5 in F Major"),
        ("7IPXZ6WYPiIAKmLGWnXXzn", "Musica Alta Ripa", "Pachelbel: Keyboard Works", "Was Gott tut, das ist wohlgetan, Partita: Choral"),
        ("1aivRKNVcjqkP86IDDr1kd", "Cantus Cölln; Konrad Junghänel", "Pachelbel: Sacred Vocal Works", "Nun danket alle Gott, P. 381"),
    ],
    "vivaldi": [
        ("3gkvR6nLCTWjMgdkETkPlT", "Itzhak Perlman; London Philharmonic Orchestra", "Vivaldi: The Four Seasons", "The Four Seasons 'Spring': I.Allegro"),
        ("5Txwlv081K39njx353jh7r", "John Eliot Gardiner; English Baroque Soloists", "Vivaldi: Gloria", "Vivaldi: Gloria in D Major, RV 589: I. Gloria in excelsis Deo"),
        ("5ROnC4xzMcQIZKlRpZlXPy", "Academy of St. Martin in the Fields; Neville Marriner", "Vivaldi: L'estro armonico", "Vivaldi: L'estro armonico, Violin Concerto in D Major, Op. 3 No. 9, RV 230: I. Allegro"),
        ("61gK8kAoXZIR5URD2pqrMv", "Academy of St. Martin in the Fields; Neville Marriner", "Vivaldi: L'estro armonico", "Concerto for 4 Violins in B Minor, Op. 3 No. 10, RV 580: I. Allegro"),
        ("4QTMkNOTAeOi5K1nok1h9T", "Itzhak Perlman; London Philharmonic Orchestra", "Vivaldi: The Four Seasons", "La Tempesta di Mare, Concerto No. 5 in E-Flat Major, RV 253: I. Presto"),
        ("5ABTu2tQsbCTd7pGIssyc5", "Emma Kirkby; Academy of Ancient Music; Christopher Hogwood", "Vivaldi: Stabat Mater", "Vivaldi: Stabat Mater, RV 621: I. Stabat Mater dolorosa"),
        ("3QGL4EbtN2iemUhvGU3imq", "I Solisti Veneti; Claudio Scimone", "Vivaldi: L'Olimpiade", "Vivaldi: L'Olimpiade, RV 725: Overture"),
        ("0QLD0h4HCckRdF3L8zmqUQ", "Ensemble Vocal Michel Corboz; Jennifer Smith", "Vivaldi: Sacred Works", "Vivaldi: Nulla in mundo pax sincera, RV 630: \"Nulla in Mundo pax sincera\""),
        ("2cq1Bvya0v5sC0FioZiiD3", "Julian Lloyd Webber; Jiaxin Lloyd Webber; Royal Philharmonic Orchestra", "Vivaldi: Concertos", "Concerto for 2 Cellos in G Minor, RV 531: I. Allegro"),
        ("2zOQgaliSdCHq4FKhB7scb", "Nigel Kennedy; English Chamber Orchestra", "Vivaldi: Il cimento dell'armonia e dell'inventione, Op. 8", "Il cimento dell'armonia e dell'inventione, Op.8: IV. Violin Concerto in F minor, RV 297"),
    ],
    "bach": [
        ("1MwVOQPwBmJFDshhtxtuER", "English Baroque Soloists; Monteverdi Choir; John Eliot Gardiner", "Bach: St. Matthew Passion, BWV 244", "Matthäus-Passion, BWV 244, Pt. 1"),
        ("5bu9A6uphPWg39RC3ZKeku", "Glenn Gould", "Bach: Goldberg Variations, BWV 988", "Goldberg Variations, BWV 988: Aria"),
        ("4yvlLkFUwdbWFzMMXSPjfU", "Glenn Gould", "Bach: The Well-Tempered Clavier, Book I", "The Well-Tempered Clavier, Book 1: Prelude No. 1 in C Major, BWV 846"),
        ("1SxPv1FwuhCmoPV5tuCswJ", "English Baroque Soloists; John Eliot Gardiner", "Bach: Brandenburg Concertos", "Brandenburg Concerto No. 1 in F Major, BWV 1046: I. —"),
        ("61dYvvfIRtIDFuqZypPAta", "Yo-Yo Ma", "Bach: Cello Suites", "Cello Suite No. 1 in G Major, BWV 1007: I. Prélude"),
        ("2HrZRlglFGo9h782g6VPp8", "English Baroque Soloists; Monteverdi Choir; John Eliot Gardiner", "Bach: Mass in B Minor", "Mass in B Minor, BWV 232: Kyrie eleison"),
        ("1Ge0iAZ692qwAR9LdlCBjl", "Karl Richter", "Bach: Organ Works", "Toccata & Fugue in D Minor, BWV 565: I. Toccata"),
        ("2poItDBXTiWIPMBbyok8xk", "Glenn Gould", "Bach: The Art of Fugue", "The Art of the Fugue, BWV 1080: Contrapunctus I"),
        ("4B9TTSnGcEWYvHbpH5AhHx", "Jascha Heifetz", "Bach: Partita No. 2, BWV 1004", "Partita No. 2 in D Minor, BWV 1004: V. Chaconne"),
        ("0VLeU5kTsQFzmYGioIGBoX", "Dietrich Fischer-Dieskau; Münchener Bach-Orchester; Karl Richter", "Bach: Cantatas", "Ich habe genug, Cantata BWV 82: 1. \"Ich habe genug, ich habe den Heiland\""),
    ],
    "handel": [
        ("3TWk0Dft5RbHufs8HjuDoD", "English Baroque Soloists; Monteverdi Choir; John Eliot Gardiner", "Handel: Messiah", "The Messiah, HWV 56 - Part 1, \"The Annunciation\": Overture (Sinfonia)"),
        ("4TQR2Z0VXSJ44olJdc4z1Y", "Academy of St. Martin in the Fields; Neville Marriner", "Handel: Water Music", "Water Music, Suite No. 1 in F Major, HWV 348: I. Overture"),
        ("4CV7FMg5jMthjKnMdcOxIl", "Academy of St. Martin in the Fields; Neville Marriner", "Handel: Music for the Royal Fireworks", "Music for the Royal Fireworks, HWV 351: I. Ouverture"),
        ("7yNiuZjOP5ESp7zirlnHXg", "Orchestra of the Age of Enlightenment; Sir Roger Norrington", "Handel: Serse", "Serse, HWV 40 / Act 1: \"Ombra mai fu\""),
        ("1B6tLHyQe8DiVBXC3UVap0", "Academy of St. Martin in the Fields; Neville Marriner", "Handel: Solomon", "Handel: Solomon, HWV 67, Act 3: Sinfonia \"The Arrival of the Queen of Sheba\""),
        ("46pUDGpgvdlj6Wl8SeKW8c", "English Baroque Soloists; Monteverdi Choir; John Eliot Gardiner", "Handel: Dixit Dominus", "Dixit Dominus, HWV 232: I. Dixit Dominus, Domino meo"),
        ("1vZ9ZNcx57COvahQxT3c7l", "Les Arts Florissants; William Christie", "Handel: Alcina", "Handel: Alcina, HWV 34: Overture (Live)"),
        ("2axNZf8KHHYOHDaqzujiWk", "Academy of Ancient Music; Andrew Manze", "Handel: Concerti grossi, Op. 6", "Concerto grosso in G Major, Op. 6 No. 1, HWV 319: I. A tempo giusto"),
        ("3e9h6wbSH3ryYrmaF5Xf0E", "David Daniels; Orchestra of the Age of Enlightenment; Sir Roger Norrington", "Handel: Giulio Cesare", "Handel: Giulio Cesare in Egitto, HWV 17, Act 1: Aria. \"Va tacito e nascosto\" (Cesare)"),
        ("11Iwzyv2vxqJHP8MCmsRUD", "Concentus Musicus Wien; Nikolaus Harnoncourt", "Handel: Saul", "Handel: Saul, HWV 53, Act 3: Dead March"),
    ],
    "haydn": [
        ("6T4dExgsUz3X6ZbK8UoGhX", "Wiener Philharmoniker; Leonard Bernstein", "Haydn: Symphonies", "Symphony No. 94 in G Major, Hob. I:94 \"Surprise\": I. Adagio – Vivace assai"),
        ("24lzMzO46Lh1tozO1ZAHPX", "London Philharmonic Orchestra; Eugen Jochum", "Haydn: Symphony No. 104", "Symphony No. 104 in D Major, Hob. I:104 \"London\": I. Adagio – Allegro"),
        ("6EWve6BCc6aiJh7k1EM9Eg", "English Baroque Soloists; Monteverdi Choir; John Eliot Gardiner", "Haydn: The Creation", "The Creation, Hob.XXI:2: Pt. 1, In the Beginning"),
        ("2JACQEqmD0WnBIHgO9P67W", "Takács Quartet", "Haydn: String Quartets, Op. 76", "String Quartet In C Major, Op.76 No.3, Hob. lll:77 \"Emperor\": II. Poco adagio, cantabile"),
        ("15Bn1PwUXgrIiO3yTk4ISl", "Håkan Hardenberger; Academy of St. Martin in the Fields; Neville Marriner", "Haydn: Trumpet Concerto", "Trumpet Concerto in E-Flat Major, Hob. VIIe:1: I. Allegro"),
        ("6DLhQVXiUgaZzfehrrBYGZ", "English Baroque Soloists; Monteverdi Choir; John Eliot Gardiner", "Haydn: The Seasons", "Die Jahreszeiten, Hob. XXI:3: No. 1, Introduction & Recit. Seht wie der strenge Winter flieht!"),
        ("0uHEOH0MTXxt3wvbQF7WIr", "Philharmonia Hungarica; Antal Doráti", "Haydn: Symphony No. 45", "Symphony No. 45 in F-Sharp Minor, Hob. I:45 \"Farewell\": IV. Finale. Presto – Adagio"),
        ("4rRgOKcsgPhmWQoHiF73T5", "Alfred Brendel", "Haydn: Piano Sonatas", "Piano Sonata in E-Flat Major, Hob. XVI:52: I. Allegro (moderato)"),
        ("6RX6xycG7TqFdFcCUH06Sh", "Coull Quartet", "Haydn: String Quartets, Op. 33", "String Quartet in E Flat Major, Op. 33 No. 2 \"The Joke\": I. Allegro moderato"),
        ("2fNr5zLAJYMd6kTmIR4O3t", "Les Arts Florissants; William Christie", "Haydn: The Seven Last Words", "Haydn: The Seven Last Words of Christ, Hob. XX:1: Introduction. Maestoso ed adagio"),
    ],
    "clementi": [
        ("4yR9oUZINEL5VXGgY2wqJo", "Peter Nagy", "Clementi: Gradus ad Parnassum", "Gradus ad Parnassum, Op. 44: No. 1, Con velocita"),
        ("46FGAXQfWwl4qj2o1yx53M", "Muzio Clementi", "Clementi: Sonatinas, Op. 36", "Sonatina Op.36 No.1"),
        ("6KbqeY4NxruW5adOFZSw8h", "Maria Tipo", "Clementi: Piano Sonatas", "Keyboard Sonata in F Minor, Op. 13 No. 6: I. Allegro agitato"),
        ("4A7S0WZz4vXM2Hv4ySPPJl", "Lazar Berman", "Clementi: Piano Sonatas", "Piano Sonata in B Minor, Op. 40, No. 2"),
        ("1smdS4OpiN9meNCEG7TSq7", "Vladimir Horowitz", "Clementi: Piano Sonatas", "Sonata, Op. 24, No. 2/Op.47, No. 2 in B-Flat: Allegro con brio (I)"),
        ("7uPCEpiMqxwzS7WFyXxID1", "Andreas Staier", "Clementi: Piano Sonatas", "Keyboard Sonata in F minor Op.13 No.6 : I Allegro agitato"),
        ("3MYLdEYMjuSNollMkuAEkK", "London Mozart Players; Matthias Bamert", "Clementi: Symphonies", "Symphony No. 3 in G Major, WoO 34, \"The Great National\": IV. Finale: Allegro vivace"),
        ("05BP90XvzX7LKsZfPns9Jp", "Peter Nagy", "Clementi: Sonatinas, Op. 36", "Clementi: Sonatina in C major, Op. 36, No. 1, Allegro"),
        ("2yOJDZlscfwFu8HBrAn6no", "Andreas Staier", "Clementi: Capriccios", "Clementi : Capriccio in B flat major Op.17"),
        ("6DkMMLb54X3nKGrwPsiIdI", "Luca Rasca", "Clementi: Piano Sonatas", "Piano Sonata No. 6 in F Minor, Op. 13: I. Allegro agitato"),
    ],
    "mozart": [
        ("1uGvImyO4nAjB3TTpTjuAT", "Wiener Philharmoniker; Karl Böhm", "Mozart: Requiem", "Requiem in D Minor, K. 626: I. Introïtus"),
        ("3icP3jAlx7m7W8Fc8p26xp", "Wiener Symphoniker; Karl Böhm", "Mozart: Le nozze di Figaro", "Le nozze di Figaro, K.492: Overture"),
        ("4b3auGge5EYekOHGyLa92s", "Philharmonia Orchestra; Carlo Maria Giulini", "Mozart: Don Giovanni", "Don Giovanni, K. 527: Overture"),
        ("3NwDG4dvFOb7svVDP3H8uz", "Berliner Philharmoniker; Karl Böhm", "Mozart: Symphonies", "Symphony No. 40 in G Minor, K. 550: I. Molto allegro"),
        ("1eCouLD4K2IkqPQ23CVlLl", "Stephen Kovacevich; London Symphony Orchestra; Sir Colin Davis", "Mozart: Piano Concertos", "Piano Concerto No. 21 in C, K.467: 2. Andante"),
        ("6yI8itfbhrlAJ6wb50H5uV", "Piotr Anderszewski; Scottish Chamber Orchestra", "Mozart: Piano Concertos", "Mozart: Piano Concerto No. 20 in D Minor, K. 466: I. Allegro"),
        ("3LntR2V8IepCX490aPUwBZ", "New York Philharmonic; Bruno Walter", "Mozart: Symphonies", "Symphony No. 41 in C Major, K. 551 \"Jupiter\": I. Allegro vivace"),
        ("6B8Rd4BNfrxpXxDAql0c26", "Karl Leister; Academy of St. Martin in the Fields; Neville Marriner", "Mozart: Clarinet Concerto", "Mozart: Clarinet Concerto in A, K.622 - 1. Allegro"),
        ("7wh752sm37VDoBtf2bsIhu", "Alban Berg Quartett; Markus Wolf", "Mozart: String Quintets", "Mozart: String Quintet No. 4 in G Minor, K. 516: I. Allegro"),
        ("20X3o1UIOEzLssNKr2rIq2", "Wiener Philharmoniker; Karl Böhm", "Mozart: Così fan tutte", "Così fan tutte, K.588: Overture"),
    ],
    "beethoven": [
        ("2TWvopA1DtWu0QaINDD1PH", "Wiener Philharmoniker; Herbert von Karajan", "Beethoven: Symphony No. 9", "Symphony No. 9 in D Minor, Op. 125 \"Choral\": I. Allegro ma non troppo, un poco maestoso"),
        ("6cUCckpdlqHJ5Ascf2uH2A", "Wiener Philharmoniker; Carlos Kleiber", "Beethoven: Symphony No. 5", "Symphony No. 5 in C Minor, Op. 67: I. Allegro con brio"),
        ("0lIiqlwsdt0stDPpaAtnP9", "Claudio Arrau", "Beethoven: Piano Sonatas", "Piano Sonata No. 14 in C-Sharp Minor, Op. 27 No. 2 \"Moonlight\": I. Adagio sostenuto"),
        ("5b5CxT1iOjfTb1WhADtE4r", "New York Philharmonic; Leonard Bernstein", "Beethoven: Symphony No. 3", "Symphony No. 3 in E-Flat Major, Op. 55 \"Eroica\": I. Allegro con brio"),
        ("3MecollVHlmOxAStFHC6tB", "Takács Quartet", "Beethoven: Late String Quartets", "String Quartet No.12 in E flat, Op.127: 1. Maestoso - Allegro"),
        ("2MyGUtp0uXf3wYRBDWdFAi", "Alfred Brendel; Wiener Philharmoniker", "Beethoven: Piano Concertos", "Piano Concerto No. 5 in E-Flat Major, Op. 73 \"Emperor\": I. Allegro"),
        ("1F5Pbq54VDIu1VHITew0dJ", "David Oistrakh; Orchestre National de France; André Cluytens", "Beethoven: Violin Concerto", "Violin Concerto in D Major, Op. 61 - I. Allegro ma non troppo"),
        ("01DRO0JwG25sKs3ibLbgHA", "Busch Quartet", "Beethoven: String Quartet Op. 131", "String Quartet No. 14 in C-Sharp Minor, Op. 131"),
        ("5Rn7DT15VV7iKh7mbfCcMJ", "Maurizio Pollini", "Beethoven: Piano Sonatas", "Piano Sonata No.32 In C Minor, Op.111: 1. Maestoso"),
        ("6Ua1yeSilCS4WZHvfW88xD", "Sir Georg Solti; London Symphony Orchestra; London Voices", "Beethoven: Missa Solemnis", "Kyrie (excerpt) from Missa Solemnis in D Major, Op. 123 - Voice"),
    ],
    "schumann": [
        ("12YOTScIhCHfCzUAKjdse5", "Vladimir Horowitz", "Schumann: Kinderszenen", "Träumerei, Op. 15 No. 7"),
        ("0Xjec9VWjmRFRXEAlrLj9c", "Vladimir Horowitz", "Schumann: Carnaval", "Carnaval, Op. 9: Préambule"),
        ("2ycx8gqFcO8UcMbx7KthuN", "Martha Argerich; Gewandhausorchester Leipzig; Riccardo Chailly", "Schumann: Piano Concerto", "Piano Concerto in A Minor, Op. 54: I. Allegro affettuoso"),
        ("34QR4cqNTV1iTyDMakeRZz", "Dietrich Fischer-Dieskau; Jörg Demus", "Schumann: Dichterliebe", "Dichterliebe, Op. 48: Im wunderschönen Monat Mai"),
        ("7dJviope9IXG1ecVHcGeMb", "New York Philharmonic; Leonard Bernstein", "Schumann: Symphonies", "Symphony No. 3 in E-Flat Major, Op. 97 \"Rhenish\": I. Lebhaft"),
        ("0foJvNiR01r3CXfXTO7YHg", "Vladimir Horowitz", "Schumann: Kreisleriana", "Kreisleriana, Op. 16: Äußerst bewegt"),
        ("1G8PAUCtTWsg5P5GUY0RKE", "Dietrich Fischer-Dieskau; Christoph Eschenbach", "Schumann: Frauenliebe und -leben", "Seit ich ihn gesehen, Op. 42 No. 1"),
        ("6EhsKprF83G7NK8vTejyC9", "Martha Argerich", "Schumann: Piano Sonatas", "Piano Sonata No. 1 in F-Sharp Minor, Op. 11: I. Introduzione: Un poco adagio – Allegro vivace"),
        ("37YQ87dqPR7RRn7SBfvmRf", "Mstislav Rostropovich; Leningrad Philharmonic Orchestra; Gennady Rozhdestvensky", "Schumann: Cello Concerto", "Cello Concerto in A Minor, Op. 129: I. Nicht zu schnell"),
        ("5rCsP7WvgsiHTN9aUHO2nq", "Martha Argerich", "Schumann: Fantasie", "Fantasie in C Major, Op. 17: I. Durchaus phantastisch und leidenschaftlich vorzutragen"),
    ],
    "chopin": [
        ("6VVk2Vpovu66hnDCQxicTC", "Arthur Rubinstein", "Chopin: Nocturnes", "Nocturne No. 2 in E-Flat Major, Op. 9 No. 2"),
        ("5A91N8OxPL3yxwdWATwP7n", "Vladimir Horowitz", "Chopin: Ballades", "Ballade No. 1 in G Minor, Op. 23"),
        ("4tGuc1jFhmel25vpmyTSNw", "Maurizio Pollini", "Chopin: Études", "Études, Op. 10: No. 12 in C Minor \"Revolutionary\""),
        ("3GUNOaiWBO0BSUmBJQBth5", "Martha Argerich", "Chopin: Piano Sonatas", "Piano Sonata No. 2 in B-Flat Minor, Op. 35: I. Grave – Doppio movimento"),
        ("3a4iO9ruBqKYx1GdHCTJiP", "Arthur Rubinstein", "Chopin: Polonaises", "Polonaise No. 6 in A-Flat Major, Op. 53 \"Heroic\""),
        ("1kVoL8Qst9UP3X902NWMo7", "Krystian Zimerman", "Chopin: Ballades", "Ballade No. 4 in F Minor, Op. 52"),
        ("70pMcM2bkNg6aHXbMvb9Da", "Arthur Rubinstein", "Chopin: Scherzos", "Scherzo No. 2 in B-Flat Minor, Op. 31"),
        ("4KdU8Qm3HPLTNGxLocWJBI", "Martha Argerich", "Chopin: Piano Sonatas", "Piano Sonata No. 3 in B Minor, Op. 58: I. Allegro maestoso"),
        ("5frCuNxx2Z6q5gvvglW9N4", "Arthur Rubinstein", "Chopin: Barcarolle", "Barcarolle in F-Sharp Major, Op. 60"),
        ("3bzsz4LOUswo61Vt0A27md", "Arthur Rubinstein", "Chopin: Mazurkas", "Mazurka in A Minor, Op. 17 No. 4"),
    ],
    "liszt": [
        ("4wNBtIdL5Klrc74b6ZF1ct", "Claudio Arrau", "Liszt: Piano Sonata", "Piano Sonata in B Minor, S. 178"),
        ("6Ks4Hz1aS9KaDvO6qltUgh", "Jorge Bolet", "Liszt: Transcendental Études, S. 139", "Transcendental Etudes, S. 139: No. 10 in F Minor"),
        ("7CIoJE0JfVFcmmUY3fFojH", "Vladimir Horowitz", "Liszt: Hungarian Rhapsody No. 2", "Hungarian Rhapsody No. 2 in C-Sharp Minor, S. 244/2"),
        ("7kSq658CO3pSblozk3QtLZ", "Berliner Philharmoniker; Herbert von Karajan", "Liszt: Les préludes", "Les préludes, Symphonic Poem No. 3, S. 97"),
        ("5qpUmfrVRpCrzjQXeouFVa", "Daniel Barenboim", "Liszt: Liebesträume", "Notturno III: O lieb, so lang du lieben kannst"),
        ("5BFX0pJamjti3WvpntzTgx", "Daniel Barenboim", "Liszt: Années de pèlerinage — Italie", "Liszt: Années de pèlerinage, Deuxième Année, Italie, S. 161: Après une lecture du Dante"),
        ("4G4WzStsJnzb8lPmhTnEa1", "Berliner Philharmoniker; Herbert von Karajan", "Liszt: Mephisto Waltz", "Mephisto Waltz No. 1, S. 110/2 (Orch. Version)"),
        ("51a92WEoWM8W02jeoPmDCf", "Daniel Barenboim", "Liszt: Années de pèlerinage — Suisse", "Années de pèlerinage I, Suisse, S. 160: I. Chapelle de Guillaume Tell"),
        ("2oT0H9WBSCAfNBSdk6eXDe", "Alfred Brendel", "Liszt: Paganini Studies", "Paganini Studies, S 141: Etude in G Sharp Minor - \"La Campanella\""),
        ("2HV3N38YY9u15H1rLLYkZD", "Pierre-Laurent Aimard", "Liszt: Via Crucis", "Jésus est condamné à mort"),
    ],
    "wagner": [
        ("0x5PgGixmeahAJHtUhwMXT", "Wiener Philharmoniker; Sir Georg Solti", "Wagner: Der Ring des Nibelungen", "Das Rheingold: Prelude - 2012 Remaster"),
        ("03TfFfReDh8T5Xm1FoC0pS", "Berliner Philharmoniker; Herbert von Karajan", "Wagner: Tristan und Isolde", "Tristan und Isolde, Act 1: Prelude"),
        ("0MsDA4lCcKo7hiVAEFJocm", "Berliner Philharmoniker; Herbert von Karajan", "Wagner: Die Meistersinger von Nürnberg", "Richard Wagner - Die Meistersinger Von Nurnberg Overture"),
        ("0hwNXf1IJiJq6up4hsyjuy", "Münchner Philharmoniker; Hans Knappertsbusch", "Wagner: Parsifal", "Parsifal: Prelude"),
        ("4971i3mX1RV6uP0iLhotBT", "Wiener Philharmoniker; Sir Georg Solti", "Wagner: Die Walküre", "Die Walküre (The Valkyrie), WWV 86b, Act 3: Ride of the Valkyries"),
        ("41ANrMN7MY8nsdaNpMgt7k", "Philharmonia Orchestra; Otto Klemperer", "Wagner: Der fliegende Holländer", "Wagner: Der fliegende Holländer: Overture"),
        ("6FjXmTG6GC6MaqBsKV3PiG", "Wiener Philharmoniker; Sir Georg Solti", "Wagner: Tannhäuser", "Tannhäuser: Overture"),
        ("6fWPnPQoGpUf5P4EMUI3Vt", "Wiener Philharmoniker; Rudolf Kempe", "Wagner: Lohengrin", "Wagner: Lohengrin, Act 1: Prelude"),
        ("0tBbHb0q0Wg0Rt44pKaUCw", "Wiener Philharmoniker; Wilhelm Furtwängler", "Wagner: Siegfried Idyll", "Siegfried-Idyll"),
        ("03ogvNDeKUTGMjcoLJcg74", "Jessye Norman; London Symphony Orchestra; Sir Colin Davis", "Wagner: Wesendonck Lieder", "Wesendonck Lieder : Der Engel"),
    ],
    "brahms": [
        ("7oj60E1kinQqExzWlRYW93", "Wiener Philharmoniker; Herbert von Karajan; Wiener Singverein", "Brahms: Ein deutsches Requiem", "Ein deutsches Requiem, Op. 45: I. Selig sind die da Leid tragen"),
        ("7ppPbH8hhYDHj58B0jlpCF", "Berliner Philharmoniker; Herbert von Karajan", "Brahms: Symphony No. 1", "Symphony No. 1 in C Minor, Op. 68: I. Un poco sostenuto – Allegro"),
        ("57DpDuvpZzuhTsRGowy86A", "Wiener Philharmoniker; Carlos Kleiber", "Brahms: Symphony No. 4", "Symphony No. 4 in E Minor, Op. 98: I. Allegro non troppo"),
        ("0XHzeK7XP8Is2LjkFo7S50", "Jascha Heifetz; Chicago Symphony Orchestra; Fritz Reiner", "Brahms: Violin Concerto", "Violin Concerto in D Major, Op. 77: I. Allegro non troppo"),
        ("1OC3OID40zmtBEtsFEA0Su", "Radu Lupu", "Brahms: 6 Piano Pieces, Op. 118", "6 Piano Pieces, Op. 118: No. 2, Intermezzo in A Major"),
        ("6P2hnVVErhgrc0W0L7CMrS", "Chicago Symphony Orchestra; Sir Georg Solti", "Brahms: Academic Festival Overture", "Academic Festival Overture, Op. 80"),
        ("1RvqI0BjPdOkV6c37Otpgs", "David Oistrakh; Mstislav Rostropovich; The Cleveland Orchestra; George Szell", "Brahms: Double Concerto", "Brahms: Double Concerto in A Minor, Op. 102: I. Allegro"),
        ("2Hran5Jw9zejs7DFg7BU8h", "Emil Gilels; Berliner Philharmoniker; Eugen Jochum", "Brahms: Piano Concerto No. 2", "Piano Concerto No. 2 in B-Flat Major, Op. 83: I. Allegro non troppo"),
        ("0FIF4fIoi4dWJubNO5vq6q", "Karl Leister; Amadeus Quartet", "Brahms: Clarinet Quintet", "Clarinet Quintet in B Minor, Op. 115: I. Allegro"),
        ("36DOn2q9g6ZFTfdRzeHVMz", "Berliner Philharmoniker; Herbert von Karajan", "Brahms: Symphony No. 2", "Symphony No. 2 in D Major, Op. 73: I. Allegro non troppo"),
    ],
    "tchaikovsky": [
        ("6IdBmiRneZPbhwRC3rYcEu", "Minnesota Orchestra; Antal Doráti", "Tchaikovsky: Swan Lake", "Swan Lake, Op. 20, TH 12: Introduction"),
        ("4sARvyH3zcpCL35nN70Gev", "Van Cliburn; RCA Symphony Orchestra; Kirill Kondrashin", "Tchaikovsky: Piano Concerto No. 1", "Tchaikovsky: Piano Concerto No. 1 in B flat minor Op. 23: Allegro con fuoco"),
        ("290BW71lnPekvmunWqFwBZ", "London Symphony Orchestra; Antal Doráti", "Tchaikovsky: The Nutcracker", "The Nutcracker Suite, Op. 71a: Miniatur - Overture"),
        ("7eo3ZEcsHedTaxlY8PINQl", "Leningrad Philharmonic Orchestra; Evgeny Mravinsky", "Tchaikovsky: Symphony No. 6", "Symphony No. 6 in B Minor, Op. 74 \"Pathétique\": I. Adagio – Allegro non troppo"),
        ("1AbMBp7jF9co7BnyPLRmec", "David Oistrakh; Philadelphia Orchestra; Eugene Ormandy", "Tchaikovsky: Violin Concerto", "Violin Concerto in D Major, Op. 35: I. Allegro moderato"),
        ("3XZ1Ecm9MdIVSFtnqAZefc", "Minnesota Orchestra; University of Minnesota Brass Band; Antal Doráti", "Tchaikovsky: 1812 Overture", "1812 Overture, Op. 49"),
        ("0MN3erUzrHFyq9dS3lzpoX", "New York Philharmonic; Leonard Bernstein", "Tchaikovsky: Romeo and Juliet", "Romeo and Juliet Fantasy Overture, TH 42"),
        ("0qRIG8F8PDkZSVAGGDMWVV", "Leningrad Philharmonic Orchestra; Evgeny Mravinsky", "Tchaikovsky: Symphony No. 5", "Symphony No. 5 in E Minor, Op. 64: I. Andante – Allegro con anima"),
        ("2sGUNLmwjfayJNfFpBdMXA", "Orchestre Symphonique de Montréal; Charles Dutoit", "Tchaikovsky: The Sleeping Beauty", "The Sleeping Beauty / Prologue: Introduction"),
        ("2ZXqPZtd0vqf9aQ0l86kvi", "Borodin Quartet", "Tchaikovsky: String Quartet No. 1", "String Quartet No. 1 in D Major, Op. 11: II. Andante cantabile"),
    ],
    "faure": [
        ("3bGywauvr6DieWkon8ja6Y", "", "", ""),
        ("2E26t2sde6VMhWOIhxdBd7", "", "", ""),
        ("63WAGVk3YHoFIV4WXhtiJD", "", "", ""),
        ("2Ms4tuKvhAECOducT5Chyr", "", "", ""),
        ("4IfZ5kVLFTJxXRQfjU8OXw", "", "", ""),
        ("4sFZ6P5BlLUovIgXeJNuYW", "", "", ""),
        ("0IhLPNXylgvhKl52xPYFWw", "", "", ""),
        ("6Ocr1TnN6WbQetmPXMW5xk", "", "", ""),
        ("3jiI9VLCZkR81uELMCDPoR", "", "", ""),
        ("4hTKDALr2iWg1k269kTene", "", "", ""),
    ],
    "debussy": [
        ("5j4r38PrBKhYUyKtkpzWG4", "", "", ""),
        ("4YrZ6iHcsaftcytVHR9fGq", "", "", ""),
        ("6shl4kq3AmiJkxExQhNj2Q", "", "", ""),
        ("2s3YB2mrDG9Tw0E9s5UMVy", "", "", ""),
        ("2UKima1uKrehle5qva7sXe", "", "", ""),
        ("6VRCCEvDGOsiOe6M6qDsBq", "", "", ""),
        ("2MSIUY6WvI480GTNurdJoF", "", "", ""),
        ("2h2oXCKmbjxa22VCHYYXQW", "", "", ""),
        ("6T00dKcg4GOQQuVOOZv0h2", "", "", ""),
        ("6ChaBDbCb7NHmU563z3kpQ", "", "", ""),
    ],
    "satie": [
        ("4nd6FMCfNFWkbi2dnsf5I3", "", "", ""),
        ("4Df5xVNKyGGAUlsD92GVTq", "", "", ""),
        ("6CN7bR7NDOGJAJVuNz8FxX", "", "", ""),
        ("0eHOw5xlTyw2DbVTHu3mlH", "", "", ""),
        ("1enw7gOZ4gNBqllsSRjRw8", "", "", ""),
        ("1ROF9qr1Zl6UuJ88JmPSed", "", "", ""),
        ("3zx3GvsSjSjtPhL8dRcPy0", "", "", ""),
        ("2kjgROv83iX1nrNAm7C8RB", "", "", ""),
        ("1DAJ7SKraue7eU4i8qLxEi", "", "", ""),
        ("1q8VRWNwgVFgIaaIbxVW82", "", "", ""),
    ],
    "ravel": [
        ("5H5rBc1eXU8uwn1KoC5uOd", "", "", ""),
        ("5zPJqEgWo15pK0sVfZAtsU", "", "", ""),
        ("6n2Zmiq8u7yAYF8ZCskfmf", "", "", ""),
        ("0NrLbOzdDJuY5krJyKDRF2", "", "", ""),
        ("3udU7v8Yu8MxghRxPfK1YK", "", "", ""),
        ("63iZl8TsApZCCVr6Kv8q23", "", "", ""),
        ("0j3CcnCP9WU9uovjzlLYg0", "", "", ""),
        ("7JcORVrh4j5kwIi5aTucUD", "", "", ""),
        ("7qdPj7bCn5RHzgqIDt3o1B", "", "", ""),
        ("5kxfgPchFNRCCY0gEuuzTi", "", "", ""),
    ],
    "schoenberg": [
        ("3PtQihklToU1YTsKrEHPSm", "", "", ""),
        ("7vDK41tTV8ZCOZ0DWpDjjV", "", "", ""),
        ("2TAC1e2MSO2f7Tm6M0AVZe", "", "", ""),
        ("0MeUtxCiO9TEHYpY0iAWuN", "", "", ""),
        ("3aLBmGiKnERrkmKyFMnv2o", "", "", ""),
        ("1xwT64tRe4ZWcuNeDV67zV", "", "", ""),
        ("208k9nC7hFn0ftlUZ3AHEt", "", "", ""),
        ("6q7RWooqfoQpSFwxo6qecC", "", "", ""),
        ("5bc8BoV3tUjRUz7LyAWNMf", "", "", ""),
        ("2YQfkCOFCMorglizirsbM6", "", "", ""),
    ],
    "bartok": [
        ("193iKswklSU5w9amrMqyDO", "", "", ""),
        ("6EAqH2X8e3gE0oj7g2hEE6", "", "", ""),
        ("1gg6l0pcEn6OmIHD9832AG", "", "", ""),
        ("6GPPGBvZrYJ1wkFSh4ztXP", "", "", ""),
        ("3SrmfWZYLG2B0I10iOuXet", "", "", ""),
        ("1tx66w2szO0oHXZgJbAsYz", "", "", ""),
        ("2cNGWqPZAHONH6aUY9Lpm8", "", "", ""),
        ("6dNCzq1QiNVdqln0L1i7uS", "", "", ""),
        ("0NnJZjkp9ohy3MSInP5YEs", "", "", ""),
        ("1wF0vA4xH1g556Iu4D4DUs", "", "", ""),
    ],
    "stravinsky": [
        ("241QY06A7ydXPL5c0WGLY0", "", "", ""),
        ("1IgmSJCNJwshfCGijDMHmn", "", "", ""),
        ("0aRVTTqvik5P7H0WrUwIhu", "", "", ""),
        ("1hAJY4B6EShDESNIuHrE1R", "", "", ""),
        ("344hPJntAks6E7wQriqu4C", "", "", ""),
        ("2z9CWKUy0Gjzxf0r6LMr1I", "", "", ""),
        ("5wTyJ6ral82Fy0oNJQ0zVL", "", "", ""),
        ("7uAam2sQ00GM9zoGCHxiLz", "", "", ""),
        ("2iW8uSdqppSXnwMJnT0Lv9", "", "", ""),
        ("6fEgCSMaFXzrrez00c70rv", "", "", ""),
    ],
    "shostakovich": [
        ("5cONrKOWd7jbjSGTZYs5Hv", "", "", ""),
        ("7DpDEeZww2nTL3dateKkR1", "", "", ""),
        ("1wHShi974xgPTkrvxYDBV1", "", "", ""),
        ("3tcorTc2qAByPxoCr8IsMx", "", "", ""),
        ("44UEVSMXC3S5TXHWIsFbty", "", "", ""),
        ("7lMVxzNNaYge4ydtya5NDo", "", "", ""),
        ("7ujlYp2EAVjkhXs36Lh96C", "", "", ""),
        ("79U2GHDKX2ZI3EKiAmwobK", "", "", ""),
        ("1YEx7bC8mxHcVWaAPWpRvk", "", "", ""),
        ("77YxBqdpjemz9UHOa9qrzB", "", "", ""),
    ],
    "glass": [
        ("2WGGP8dkbHANSCTA4eDoQa", "", "", ""),
        ("4N7h4IHWRaJCOo1VFdTMHV", "", "", ""),
        ("2vHxeotyQDiCsKaYsaDG5P", "", "", ""),
        ("2XYEu7Deyz20WeL6Py3XLc", "", "", ""),
        ("3FsCitB8Jg6MCiUrj7L5q8", "", "", ""),
        ("4rHUWRmjuySmgQ01vEyU8j", "", "", ""),
        ("0zXIJtldTNwGZ6jhqoOA3F", "", "", ""),
        ("1bBDENtZSmm4HQ8MGvIGOb", "", "", ""),
        ("4lKJwsEeDsBjyvzDrRa1sg", "", "", ""),
        ("1ytpHUZWEA8ViFwQFVFDDH", "", "", ""),
    ],
}

def tid_ok(tid: str) -> bool:
    if not re.fullmatch(r"[0-9A-Za-z]{22}", tid):
        return False
    url = f"https://open.spotify.com/oembed?url=https://open.spotify.com/track/{tid}"
    try:
        out = subprocess.check_output(
            ["curl", "-sL", "-A", "Mozilla/5.0", url], timeout=25
        )
        d = json.loads(out)
        return bool(d.get("title"))
    except Exception:
        return False


OG_TITLE = re.compile(r'<meta\s+property="og:title"\s+content="([^"]*)"')
MUSIC_ALBUM = re.compile(
    r'<meta\s+name="music:album"\s+content="https://open\.spotify\.com/album/([0-9A-Za-z]{22})"'
)
DESC_ARTIST = re.compile(
    r'Listen to .+? on Spotify\. Song · (.+?) · \d{4}', re.DOTALL
)


def curl_page(url: str) -> str:
    return subprocess.check_output(
        ["curl", "-sL", "-A", "Mozilla/5.0", url], text=True, timeout=60
    )


def spotify_meta_for_track(tid: str) -> tuple[str, str, str]:
    """Return (performer, album_title, track_title) from public Spotify pages."""
    tp = curl_page(f"https://open.spotify.com/track/{tid}")
    m = OG_TITLE.search(tp)
    if not m:
        raise RuntimeError(f"no og:title for track {tid}")
    track_title = html_lib.unescape(m.group(1))
    m2 = DESC_ARTIST.search(tp)
    performer = html_lib.unescape(m2.group(1).strip()) if m2 else ""
    m3 = MUSIC_ALBUM.search(tp)
    album_title = ""
    if m3:
        ap = curl_page(f"https://open.spotify.com/album/{m3.group(1)}")
        ma = OG_TITLE.search(ap)
        if ma:
            raw = html_lib.unescape(ma.group(1)).replace(" | Spotify", "").strip()
            if " - Album by " in raw:
                raw = raw.split(" - Album by ", 1)[0].strip()
            album_title = raw
    if not performer:
        performer = "Unknown Artist"
    if not album_title:
        album_title = "Unknown Album"
    return performer, album_title, track_title


def main() -> None:
    missing = [k for k in ORDER if k not in ROWS or len(ROWS[k]) != 10]
    if missing:
        print("INCOMPLETE ROWS:", missing, file=sys.stderr)
        sys.exit(1)
    out_obj = {}
    for cid in ORDER:
        with open(os.path.join(BASE, f"{cid}.json"), encoding="utf-8") as f:
            comp = json.load(f)
        scores = [x["nameEn"] for x in comp["famousScores"]]
        rows = ROWS[cid]
        arr = []
        for i, (tid, _perf, _alb, _ttitle) in enumerate(rows):
            if os.environ.get("SKIP_SPOTIFY_VERIFY") != "1" and not tid_ok(tid):
                print(f"BAD TID {cid}[{i}] {tid}", file=sys.stderr)
                sys.exit(2)
            perf, alb, ttitle = spotify_meta_for_track(tid)
            arr.append(
                {
                    "canonicalPerformer": perf,
                    "canonicalAlbum": alb,
                    "canonicalTrackTitle": ttitle,
                    "canonicalSpotifyTrackId": tid,
                    "_workTitleEn": scores[i],
                }
            )
        out_obj[cid] = arr
    # strip debug
    for cid in ORDER:
        for o in out_obj[cid]:
            o.pop("_workTitleEn", None)
    with open(OUT, "w", encoding="utf-8") as f:
        json.dump(out_obj, f, ensure_ascii=False, indent=2)
        f.write("\n")
    print("wrote", OUT)


if __name__ == "__main__":
    main()
