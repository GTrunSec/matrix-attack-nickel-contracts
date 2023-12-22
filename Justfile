schemas_dir := "schemas"

alias j := justfmt

justfmt:
    just --fmt --unstable

ocsf:
    python script.py --source ./{{ schemas_dir }}/ocsf-schema --output ./ocsf
