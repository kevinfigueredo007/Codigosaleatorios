package system.authz

default allow := false

allow if {
    input.identity == "meu-token"
}