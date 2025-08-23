% Crime Type
crime_type(assassinat).
crime_type(vol).
crime_type(escroquerie).

% Règles
is_guilty(Suspect, vol) :-
    has_motive(Suspect, vol),
    was_near_crime_scene(Suspect, vol),
    has_fingerprint_on_weapon(Suspect, vol).
   

is_guilty(Suspect, assassinat) :-
    has_motive(Suspect, assassinat),
    was_near_crime_scene(Suspect, assassinat),
    ( has_fingerprint_on_weapon(Suspect, assassinat)
    ; eyewitness_identification(Suspect, assassinat)
    ).

is_guilty(Suspect, escroquerie) :-
    has_motive(Suspect, escroquerie),
    ( has_bank_transaction(Suspect, escroquerie)
    ; owns_fake_identity(Suspect, escroquerie)
    ).

% Entrée principale
main :-
    current_input(Input),
    read(Input, crime(Suspect, CrimeType)),
    (   
        is_guilty(Suspect, CrimeType) ->
        writeln(guilty)
        ; writeln(not_guilty)
    ),
    halt.