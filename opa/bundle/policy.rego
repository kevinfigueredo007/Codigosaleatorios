package authz

default allow := false

allow if {
    input.user in data.admins
}


allow if {
    input.user.role == "operator"
    input.action == "restart_instance"
}