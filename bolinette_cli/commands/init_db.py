def init_db(parser, seed, **_):
    parser.blnt.run_command('init_db', run_seeders=seed)
