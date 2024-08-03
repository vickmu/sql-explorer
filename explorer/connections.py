

# To support user-configured database connections that can be managed through the Explorer UI, *as well* as the
# 'legacy' connections that are configured in Django's normal settings.DATABASES config, we stitch together the two.

# We allow queries to be associated with either type of connection, seamlessly.

# The approach is to allow users to create connections with approximately the same parameters that a settings.DATABASE
# would expect. We then stitch them together into one list. When Explorer needs to access a connection, it coughs up a
# Django DatabaseWrapper connection in either case (natively, if it's coming from settings.DATABASES, or by taking the
# user-created connection and running it through the create_django_style_connection() function in this file).

# In general, amazingly, this "just works" and the entire application is perfectly happy to use either type as a
# connection. The exception to this is that there are a few bits of code that ultimately (or directly) use the
# django.db.transaction.atomic context manager. For some reason that particular Django innard takes an *alias*, not a
# proper connection. Then it retrieves the connection based on that alias. But of course if we are providing a
# user-created connection alias, Django doesn't find it (because it is looking in settings.DATABASES).

# The solution is to monkey-patch the get_connection function that transaction.atomic uses, to make it aware of the
# user-created connections.


