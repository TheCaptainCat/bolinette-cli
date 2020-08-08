def create_user(parser, *, username, email, roles):
    parser.blnt.run_command('init_db', username=username, email=email, roles=roles)
