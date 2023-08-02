# mateapp-directory #
MateApp Directory is a simple directory for workgroups that want to share a contact database but are neither willing to deploy a CRM, nor they find practical the contact sharing capabilities of other tools, or they need a complementary tool for contacts not to be shared in a CRM.

__Features:__
- Loose from validation. `First Name:` John, `Position:` Plumber, `Cell Phone:` 1-300-000-000 will validate, `Last Name:` Doe, `email:` jdoe@doetheplumber.com will also. Both empty `First Name` & `Last Name` won't.
- Minimalist Bootstrap interface.
- REST endpoint.
- Trigram similarity search, best for misspelled names.

__Installation:__
MateApp Directory is a Django stack application. PostgreSQL is the only DB supported. Deploy a Django stack app is beyond the scope ot this document.
However, note:
1. __pg_trgm__ extension must be enabled in your Postgres Database.
2. `/mateapp/settings.py.example` should be renamed to `settings.py` and modified for your deployment.


