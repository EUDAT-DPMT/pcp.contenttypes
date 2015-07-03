Introduction
============

This is a full-blown functional test. The emphasis here is on testing what
the user may input and see, and the system is largely tested as a black box.
We use PloneTestCase to set up this test as well, so we have a full Plone site
to play with. We *can* inspect the state of the portal, e.g. using 
self.portal and self.folder, but it is often frowned upon since you are not
treating the system as a black box. Also, if you, for example, log in or set
roles using calls like self.setRoles(), these are not reflected in the test
browser, which runs as a separate session.

Being a doctest, we can tell a story here.

First, we must perform some setup. We use the testbrowser that is shipped
with Five, as this provides proper Zope 2 integration. Most of the 
documentation, though, is in the underlying zope.testbrower package.

    >>> from Products.Five.testbrowser import Browser
    >>> browser = Browser()
    >>> portal_url = self.portal.absolute_url()

The following is useful when writing and debugging testbrowser tests. It lets
us see all error messages in the error_log.

    >>> self.portal.error_log._ignored_exceptions = ()

With that in place, we can go to the portal front page and log in. We will
do this using the default user from PloneTestCase:

    >>> from Products.PloneTestCase.setup import portal_owner, default_password

Because add-on themes or products may remove or hide the login portlet, this test will use the login form that comes with plone.  

    >>> browser.open(portal_url + '/login_form')
    >>> browser.getControl(name='__ac_name').value = portal_owner
    >>> browser.getControl(name='__ac_password').value = default_password
    >>> browser.getControl(name='submit').click()

Here, we set the value of the fields on the login form and then simulate a
submit click.  We then ensure that we get the friendly logged-in message:

    >>> "You are now logged in" in browser.contents
    True

Finally, let's return to the front page of our site before continuing

    >>> browser.open(portal_url)

-*- extra stuff goes here -*-
The Environment content type
===============================

In this section we are tesing the Environment content type by performing
basic operations like adding, updadating and deleting Environment content
items.

Adding a new Environment content item
--------------------------------

We use the 'Add new' menu to add a new content item.

    >>> browser.getLink('Add new').click()

Then we select the type of item we want to add. In this case we select
'Environment' and click the 'Add' button to get to the add form.

    >>> browser.getControl('Environment').click()
    >>> browser.getControl(name='form.button.Add').click()
    >>> 'Environment' in browser.contents
    True

Now we fill the form and submit it.

    >>> browser.getControl(name='title').value = 'Environment Sample'
    >>> browser.getControl('Save').click()
    >>> 'Changes saved' in browser.contents
    True

And we are done! We added a new 'Environment' content item to the portal.

Updating an existing Environment content item
---------------------------------------

Let's click on the 'edit' tab and update the object attribute values.

    >>> browser.getLink('Edit').click()
    >>> browser.getControl(name='title').value = 'New Environment Sample'
    >>> browser.getControl('Save').click()

We check that the changes were applied.

    >>> 'Changes saved' in browser.contents
    True
    >>> 'New Environment Sample' in browser.contents
    True

Removing a/an Environment content item
--------------------------------

If we go to the home page, we can see a tab with the 'New Environment
Sample' title in the global navigation tabs.

    >>> browser.open(portal_url)
    >>> 'New Environment Sample' in browser.contents
    True

Now we are going to delete the 'New Environment Sample' object. First we
go to the contents tab and select the 'New Environment Sample' for
deletion.

    >>> browser.getLink('Contents').click()
    >>> browser.getControl('New Environment Sample').click()

We click on the 'Delete' button.

    >>> browser.getControl('Delete').click()
    >>> 'Item(s) deleted' in browser.contents
    True

So, if we go back to the home page, there is no longer a 'New Environment
Sample' tab.

    >>> browser.open(portal_url)
    >>> 'New Environment Sample' in browser.contents
    False

Adding a new Environment content item as contributor
------------------------------------------------

Not only site managers are allowed to add Environment content items, but
also site contributors.

Let's logout and then login as 'contributor', a portal member that has the
contributor role assigned.

    >>> browser.getLink('Log out').click()
    >>> browser.open(portal_url + '/login_form')
    >>> browser.getControl(name='__ac_name').value = 'contributor'
    >>> browser.getControl(name='__ac_password').value = default_password
    >>> browser.getControl(name='submit').click()
    >>> browser.open(portal_url)

We use the 'Add new' menu to add a new content item.

    >>> browser.getLink('Add new').click()

We select 'Environment' and click the 'Add' button to get to the add form.

    >>> browser.getControl('Environment').click()
    >>> browser.getControl(name='form.button.Add').click()
    >>> 'Environment' in browser.contents
    True

Now we fill the form and submit it.

    >>> browser.getControl(name='title').value = 'Environment Sample'
    >>> browser.getControl('Save').click()
    >>> 'Changes saved' in browser.contents
    True

Done! We added a new Environment content item logged in as contributor.

Finally, let's login back as manager.

    >>> browser.getLink('Log out').click()
    >>> browser.open(portal_url + '/login_form')
    >>> browser.getControl(name='__ac_name').value = portal_owner
    >>> browser.getControl(name='__ac_password').value = default_password
    >>> browser.getControl(name='submit').click()
    >>> browser.open(portal_url)


The Provider content type
===============================

In this section we are tesing the Provider content type by performing
basic operations like adding, updadating and deleting Provider content
items.

Adding a new Provider content item
--------------------------------

We use the 'Add new' menu to add a new content item.

    >>> browser.getLink('Add new').click()

Then we select the type of item we want to add. In this case we select
'Provider' and click the 'Add' button to get to the add form.

    >>> browser.getControl('Provider').click()
    >>> browser.getControl(name='form.button.Add').click()
    >>> 'Provider' in browser.contents
    True

Now we fill the form and submit it.

    >>> browser.getControl(name='title').value = 'Provider Sample'
    >>> browser.getControl('Save').click()
    >>> 'Changes saved' in browser.contents
    True

And we are done! We added a new 'Provider' content item to the portal.

Updating an existing Provider content item
---------------------------------------

Let's click on the 'edit' tab and update the object attribute values.

    >>> browser.getLink('Edit').click()
    >>> browser.getControl(name='title').value = 'New Provider Sample'
    >>> browser.getControl('Save').click()

We check that the changes were applied.

    >>> 'Changes saved' in browser.contents
    True
    >>> 'New Provider Sample' in browser.contents
    True

Removing a/an Provider content item
--------------------------------

If we go to the home page, we can see a tab with the 'New Provider
Sample' title in the global navigation tabs.

    >>> browser.open(portal_url)
    >>> 'New Provider Sample' in browser.contents
    True

Now we are going to delete the 'New Provider Sample' object. First we
go to the contents tab and select the 'New Provider Sample' for
deletion.

    >>> browser.getLink('Contents').click()
    >>> browser.getControl('New Provider Sample').click()

We click on the 'Delete' button.

    >>> browser.getControl('Delete').click()
    >>> 'Item(s) deleted' in browser.contents
    True

So, if we go back to the home page, there is no longer a 'New Provider
Sample' tab.

    >>> browser.open(portal_url)
    >>> 'New Provider Sample' in browser.contents
    False

Adding a new Provider content item as contributor
------------------------------------------------

Not only site managers are allowed to add Provider content items, but
also site contributors.

Let's logout and then login as 'contributor', a portal member that has the
contributor role assigned.

    >>> browser.getLink('Log out').click()
    >>> browser.open(portal_url + '/login_form')
    >>> browser.getControl(name='__ac_name').value = 'contributor'
    >>> browser.getControl(name='__ac_password').value = default_password
    >>> browser.getControl(name='submit').click()
    >>> browser.open(portal_url)

We use the 'Add new' menu to add a new content item.

    >>> browser.getLink('Add new').click()

We select 'Provider' and click the 'Add' button to get to the add form.

    >>> browser.getControl('Provider').click()
    >>> browser.getControl(name='form.button.Add').click()
    >>> 'Provider' in browser.contents
    True

Now we fill the form and submit it.

    >>> browser.getControl(name='title').value = 'Provider Sample'
    >>> browser.getControl('Save').click()
    >>> 'Changes saved' in browser.contents
    True

Done! We added a new Provider content item logged in as contributor.

Finally, let's login back as manager.

    >>> browser.getLink('Log out').click()
    >>> browser.open(portal_url + '/login_form')
    >>> browser.getControl(name='__ac_name').value = portal_owner
    >>> browser.getControl(name='__ac_password').value = default_password
    >>> browser.getControl(name='submit').click()
    >>> browser.open(portal_url)


The Person content type
===============================

In this section we are tesing the Person content type by performing
basic operations like adding, updadating and deleting Person content
items.

Adding a new Person content item
--------------------------------

We use the 'Add new' menu to add a new content item.

    >>> browser.getLink('Add new').click()

Then we select the type of item we want to add. In this case we select
'Person' and click the 'Add' button to get to the add form.

    >>> browser.getControl('Person').click()
    >>> browser.getControl(name='form.button.Add').click()
    >>> 'Person' in browser.contents
    True

Now we fill the form and submit it.

    >>> browser.getControl(name='title').value = 'Person Sample'
    >>> browser.getControl('Save').click()
    >>> 'Changes saved' in browser.contents
    True

And we are done! We added a new 'Person' content item to the portal.

Updating an existing Person content item
---------------------------------------

Let's click on the 'edit' tab and update the object attribute values.

    >>> browser.getLink('Edit').click()
    >>> browser.getControl(name='title').value = 'New Person Sample'
    >>> browser.getControl('Save').click()

We check that the changes were applied.

    >>> 'Changes saved' in browser.contents
    True
    >>> 'New Person Sample' in browser.contents
    True

Removing a/an Person content item
--------------------------------

If we go to the home page, we can see a tab with the 'New Person
Sample' title in the global navigation tabs.

    >>> browser.open(portal_url)
    >>> 'New Person Sample' in browser.contents
    True

Now we are going to delete the 'New Person Sample' object. First we
go to the contents tab and select the 'New Person Sample' for
deletion.

    >>> browser.getLink('Contents').click()
    >>> browser.getControl('New Person Sample').click()

We click on the 'Delete' button.

    >>> browser.getControl('Delete').click()
    >>> 'Item(s) deleted' in browser.contents
    True

So, if we go back to the home page, there is no longer a 'New Person
Sample' tab.

    >>> browser.open(portal_url)
    >>> 'New Person Sample' in browser.contents
    False

Adding a new Person content item as contributor
------------------------------------------------

Not only site managers are allowed to add Person content items, but
also site contributors.

Let's logout and then login as 'contributor', a portal member that has the
contributor role assigned.

    >>> browser.getLink('Log out').click()
    >>> browser.open(portal_url + '/login_form')
    >>> browser.getControl(name='__ac_name').value = 'contributor'
    >>> browser.getControl(name='__ac_password').value = default_password
    >>> browser.getControl(name='submit').click()
    >>> browser.open(portal_url)

We use the 'Add new' menu to add a new content item.

    >>> browser.getLink('Add new').click()

We select 'Person' and click the 'Add' button to get to the add form.

    >>> browser.getControl('Person').click()
    >>> browser.getControl(name='form.button.Add').click()
    >>> 'Person' in browser.contents
    True

Now we fill the form and submit it.

    >>> browser.getControl(name='title').value = 'Person Sample'
    >>> browser.getControl('Save').click()
    >>> 'Changes saved' in browser.contents
    True

Done! We added a new Person content item logged in as contributor.

Finally, let's login back as manager.

    >>> browser.getLink('Log out').click()
    >>> browser.open(portal_url + '/login_form')
    >>> browser.getControl(name='__ac_name').value = portal_owner
    >>> browser.getControl(name='__ac_password').value = default_password
    >>> browser.getControl(name='submit').click()
    >>> browser.open(portal_url)


The Resource content type
===============================

In this section we are tesing the Resource content type by performing
basic operations like adding, updadating and deleting Resource content
items.

Adding a new Resource content item
--------------------------------

We use the 'Add new' menu to add a new content item.

    >>> browser.getLink('Add new').click()

Then we select the type of item we want to add. In this case we select
'Resource' and click the 'Add' button to get to the add form.

    >>> browser.getControl('Resource').click()
    >>> browser.getControl(name='form.button.Add').click()
    >>> 'Resource' in browser.contents
    True

Now we fill the form and submit it.

    >>> browser.getControl(name='title').value = 'Resource Sample'
    >>> browser.getControl('Save').click()
    >>> 'Changes saved' in browser.contents
    True

And we are done! We added a new 'Resource' content item to the portal.

Updating an existing Resource content item
---------------------------------------

Let's click on the 'edit' tab and update the object attribute values.

    >>> browser.getLink('Edit').click()
    >>> browser.getControl(name='title').value = 'New Resource Sample'
    >>> browser.getControl('Save').click()

We check that the changes were applied.

    >>> 'Changes saved' in browser.contents
    True
    >>> 'New Resource Sample' in browser.contents
    True

Removing a/an Resource content item
--------------------------------

If we go to the home page, we can see a tab with the 'New Resource
Sample' title in the global navigation tabs.

    >>> browser.open(portal_url)
    >>> 'New Resource Sample' in browser.contents
    True

Now we are going to delete the 'New Resource Sample' object. First we
go to the contents tab and select the 'New Resource Sample' for
deletion.

    >>> browser.getLink('Contents').click()
    >>> browser.getControl('New Resource Sample').click()

We click on the 'Delete' button.

    >>> browser.getControl('Delete').click()
    >>> 'Item(s) deleted' in browser.contents
    True

So, if we go back to the home page, there is no longer a 'New Resource
Sample' tab.

    >>> browser.open(portal_url)
    >>> 'New Resource Sample' in browser.contents
    False

Adding a new Resource content item as contributor
------------------------------------------------

Not only site managers are allowed to add Resource content items, but
also site contributors.

Let's logout and then login as 'contributor', a portal member that has the
contributor role assigned.

    >>> browser.getLink('Log out').click()
    >>> browser.open(portal_url + '/login_form')
    >>> browser.getControl(name='__ac_name').value = 'contributor'
    >>> browser.getControl(name='__ac_password').value = default_password
    >>> browser.getControl(name='submit').click()
    >>> browser.open(portal_url)

We use the 'Add new' menu to add a new content item.

    >>> browser.getLink('Add new').click()

We select 'Resource' and click the 'Add' button to get to the add form.

    >>> browser.getControl('Resource').click()
    >>> browser.getControl(name='form.button.Add').click()
    >>> 'Resource' in browser.contents
    True

Now we fill the form and submit it.

    >>> browser.getControl(name='title').value = 'Resource Sample'
    >>> browser.getControl('Save').click()
    >>> 'Changes saved' in browser.contents
    True

Done! We added a new Resource content item logged in as contributor.

Finally, let's login back as manager.

    >>> browser.getLink('Log out').click()
    >>> browser.open(portal_url + '/login_form')
    >>> browser.getControl(name='__ac_name').value = portal_owner
    >>> browser.getControl(name='__ac_password').value = default_password
    >>> browser.getControl(name='submit').click()
    >>> browser.open(portal_url)


The Center content type
===============================

In this section we are tesing the Center content type by performing
basic operations like adding, updadating and deleting Center content
items.

Adding a new Center content item
--------------------------------

We use the 'Add new' menu to add a new content item.

    >>> browser.getLink('Add new').click()

Then we select the type of item we want to add. In this case we select
'Center' and click the 'Add' button to get to the add form.

    >>> browser.getControl('Center').click()
    >>> browser.getControl(name='form.button.Add').click()
    >>> 'Center' in browser.contents
    True

Now we fill the form and submit it.

    >>> browser.getControl(name='title').value = 'Center Sample'
    >>> browser.getControl('Save').click()
    >>> 'Changes saved' in browser.contents
    True

And we are done! We added a new 'Center' content item to the portal.

Updating an existing Center content item
---------------------------------------

Let's click on the 'edit' tab and update the object attribute values.

    >>> browser.getLink('Edit').click()
    >>> browser.getControl(name='title').value = 'New Center Sample'
    >>> browser.getControl('Save').click()

We check that the changes were applied.

    >>> 'Changes saved' in browser.contents
    True
    >>> 'New Center Sample' in browser.contents
    True

Removing a/an Center content item
--------------------------------

If we go to the home page, we can see a tab with the 'New Center
Sample' title in the global navigation tabs.

    >>> browser.open(portal_url)
    >>> 'New Center Sample' in browser.contents
    True

Now we are going to delete the 'New Center Sample' object. First we
go to the contents tab and select the 'New Center Sample' for
deletion.

    >>> browser.getLink('Contents').click()
    >>> browser.getControl('New Center Sample').click()

We click on the 'Delete' button.

    >>> browser.getControl('Delete').click()
    >>> 'Item(s) deleted' in browser.contents
    True

So, if we go back to the home page, there is no longer a 'New Center
Sample' tab.

    >>> browser.open(portal_url)
    >>> 'New Center Sample' in browser.contents
    False

Adding a new Center content item as contributor
------------------------------------------------

Not only site managers are allowed to add Center content items, but
also site contributors.

Let's logout and then login as 'contributor', a portal member that has the
contributor role assigned.

    >>> browser.getLink('Log out').click()
    >>> browser.open(portal_url + '/login_form')
    >>> browser.getControl(name='__ac_name').value = 'contributor'
    >>> browser.getControl(name='__ac_password').value = default_password
    >>> browser.getControl(name='submit').click()
    >>> browser.open(portal_url)

We use the 'Add new' menu to add a new content item.

    >>> browser.getLink('Add new').click()

We select 'Center' and click the 'Add' button to get to the add form.

    >>> browser.getControl('Center').click()
    >>> browser.getControl(name='form.button.Add').click()
    >>> 'Center' in browser.contents
    True

Now we fill the form and submit it.

    >>> browser.getControl(name='title').value = 'Center Sample'
    >>> browser.getControl('Save').click()
    >>> 'Changes saved' in browser.contents
    True

Done! We added a new Center content item logged in as contributor.

Finally, let's login back as manager.

    >>> browser.getLink('Log out').click()
    >>> browser.open(portal_url + '/login_form')
    >>> browser.getControl(name='__ac_name').value = portal_owner
    >>> browser.getControl(name='__ac_password').value = default_password
    >>> browser.getControl(name='submit').click()
    >>> browser.open(portal_url)


The Community content type
===============================

In this section we are tesing the Community content type by performing
basic operations like adding, updadating and deleting Community content
items.

Adding a new Community content item
--------------------------------

We use the 'Add new' menu to add a new content item.

    >>> browser.getLink('Add new').click()

Then we select the type of item we want to add. In this case we select
'Community' and click the 'Add' button to get to the add form.

    >>> browser.getControl('Community').click()
    >>> browser.getControl(name='form.button.Add').click()
    >>> 'Community' in browser.contents
    True

Now we fill the form and submit it.

    >>> browser.getControl(name='title').value = 'Community Sample'
    >>> browser.getControl('Save').click()
    >>> 'Changes saved' in browser.contents
    True

And we are done! We added a new 'Community' content item to the portal.

Updating an existing Community content item
---------------------------------------

Let's click on the 'edit' tab and update the object attribute values.

    >>> browser.getLink('Edit').click()
    >>> browser.getControl(name='title').value = 'New Community Sample'
    >>> browser.getControl('Save').click()

We check that the changes were applied.

    >>> 'Changes saved' in browser.contents
    True
    >>> 'New Community Sample' in browser.contents
    True

Removing a/an Community content item
--------------------------------

If we go to the home page, we can see a tab with the 'New Community
Sample' title in the global navigation tabs.

    >>> browser.open(portal_url)
    >>> 'New Community Sample' in browser.contents
    True

Now we are going to delete the 'New Community Sample' object. First we
go to the contents tab and select the 'New Community Sample' for
deletion.

    >>> browser.getLink('Contents').click()
    >>> browser.getControl('New Community Sample').click()

We click on the 'Delete' button.

    >>> browser.getControl('Delete').click()
    >>> 'Item(s) deleted' in browser.contents
    True

So, if we go back to the home page, there is no longer a 'New Community
Sample' tab.

    >>> browser.open(portal_url)
    >>> 'New Community Sample' in browser.contents
    False

Adding a new Community content item as contributor
------------------------------------------------

Not only site managers are allowed to add Community content items, but
also site contributors.

Let's logout and then login as 'contributor', a portal member that has the
contributor role assigned.

    >>> browser.getLink('Log out').click()
    >>> browser.open(portal_url + '/login_form')
    >>> browser.getControl(name='__ac_name').value = 'contributor'
    >>> browser.getControl(name='__ac_password').value = default_password
    >>> browser.getControl(name='submit').click()
    >>> browser.open(portal_url)

We use the 'Add new' menu to add a new content item.

    >>> browser.getLink('Add new').click()

We select 'Community' and click the 'Add' button to get to the add form.

    >>> browser.getControl('Community').click()
    >>> browser.getControl(name='form.button.Add').click()
    >>> 'Community' in browser.contents
    True

Now we fill the form and submit it.

    >>> browser.getControl(name='title').value = 'Community Sample'
    >>> browser.getControl('Save').click()
    >>> 'Changes saved' in browser.contents
    True

Done! We added a new Community content item logged in as contributor.

Finally, let's login back as manager.

    >>> browser.getLink('Log out').click()
    >>> browser.open(portal_url + '/login_form')
    >>> browser.getControl(name='__ac_name').value = portal_owner
    >>> browser.getControl(name='__ac_password').value = default_password
    >>> browser.getControl(name='submit').click()
    >>> browser.open(portal_url)


The Project content type
===============================

In this section we are tesing the Project content type by performing
basic operations like adding, updadating and deleting Project content
items.

Adding a new Project content item
--------------------------------

We use the 'Add new' menu to add a new content item.

    >>> browser.getLink('Add new').click()

Then we select the type of item we want to add. In this case we select
'Project' and click the 'Add' button to get to the add form.

    >>> browser.getControl('Project').click()
    >>> browser.getControl(name='form.button.Add').click()
    >>> 'Project' in browser.contents
    True

Now we fill the form and submit it.

    >>> browser.getControl(name='title').value = 'Project Sample'
    >>> browser.getControl('Save').click()
    >>> 'Changes saved' in browser.contents
    True

And we are done! We added a new 'Project' content item to the portal.

Updating an existing Project content item
---------------------------------------

Let's click on the 'edit' tab and update the object attribute values.

    >>> browser.getLink('Edit').click()
    >>> browser.getControl(name='title').value = 'New Project Sample'
    >>> browser.getControl('Save').click()

We check that the changes were applied.

    >>> 'Changes saved' in browser.contents
    True
    >>> 'New Project Sample' in browser.contents
    True

Removing a/an Project content item
--------------------------------

If we go to the home page, we can see a tab with the 'New Project
Sample' title in the global navigation tabs.

    >>> browser.open(portal_url)
    >>> 'New Project Sample' in browser.contents
    True

Now we are going to delete the 'New Project Sample' object. First we
go to the contents tab and select the 'New Project Sample' for
deletion.

    >>> browser.getLink('Contents').click()
    >>> browser.getControl('New Project Sample').click()

We click on the 'Delete' button.

    >>> browser.getControl('Delete').click()
    >>> 'Item(s) deleted' in browser.contents
    True

So, if we go back to the home page, there is no longer a 'New Project
Sample' tab.

    >>> browser.open(portal_url)
    >>> 'New Project Sample' in browser.contents
    False

Adding a new Project content item as contributor
------------------------------------------------

Not only site managers are allowed to add Project content items, but
also site contributors.

Let's logout and then login as 'contributor', a portal member that has the
contributor role assigned.

    >>> browser.getLink('Log out').click()
    >>> browser.open(portal_url + '/login_form')
    >>> browser.getControl(name='__ac_name').value = 'contributor'
    >>> browser.getControl(name='__ac_password').value = default_password
    >>> browser.getControl(name='submit').click()
    >>> browser.open(portal_url)

We use the 'Add new' menu to add a new content item.

    >>> browser.getLink('Add new').click()

We select 'Project' and click the 'Add' button to get to the add form.

    >>> browser.getControl('Project').click()
    >>> browser.getControl(name='form.button.Add').click()
    >>> 'Project' in browser.contents
    True

Now we fill the form and submit it.

    >>> browser.getControl(name='title').value = 'Project Sample'
    >>> browser.getControl('Save').click()
    >>> 'Changes saved' in browser.contents
    True

Done! We added a new Project content item logged in as contributor.

Finally, let's login back as manager.

    >>> browser.getLink('Log out').click()
    >>> browser.open(portal_url + '/login_form')
    >>> browser.getControl(name='__ac_name').value = portal_owner
    >>> browser.getControl(name='__ac_password').value = default_password
    >>> browser.getControl(name='submit').click()
    >>> browser.open(portal_url)


The Service content type
===============================

In this section we are tesing the Service content type by performing
basic operations like adding, updadating and deleting Service content
items.

Adding a new Service content item
--------------------------------

We use the 'Add new' menu to add a new content item.

    >>> browser.getLink('Add new').click()

Then we select the type of item we want to add. In this case we select
'Service' and click the 'Add' button to get to the add form.

    >>> browser.getControl('Service').click()
    >>> browser.getControl(name='form.button.Add').click()
    >>> 'Service' in browser.contents
    True

Now we fill the form and submit it.

    >>> browser.getControl(name='title').value = 'Service Sample'
    >>> browser.getControl('Save').click()
    >>> 'Changes saved' in browser.contents
    True

And we are done! We added a new 'Service' content item to the portal.

Updating an existing Service content item
---------------------------------------

Let's click on the 'edit' tab and update the object attribute values.

    >>> browser.getLink('Edit').click()
    >>> browser.getControl(name='title').value = 'New Service Sample'
    >>> browser.getControl('Save').click()

We check that the changes were applied.

    >>> 'Changes saved' in browser.contents
    True
    >>> 'New Service Sample' in browser.contents
    True

Removing a/an Service content item
--------------------------------

If we go to the home page, we can see a tab with the 'New Service
Sample' title in the global navigation tabs.

    >>> browser.open(portal_url)
    >>> 'New Service Sample' in browser.contents
    True

Now we are going to delete the 'New Service Sample' object. First we
go to the contents tab and select the 'New Service Sample' for
deletion.

    >>> browser.getLink('Contents').click()
    >>> browser.getControl('New Service Sample').click()

We click on the 'Delete' button.

    >>> browser.getControl('Delete').click()
    >>> 'Item(s) deleted' in browser.contents
    True

So, if we go back to the home page, there is no longer a 'New Service
Sample' tab.

    >>> browser.open(portal_url)
    >>> 'New Service Sample' in browser.contents
    False

Adding a new Service content item as contributor
------------------------------------------------

Not only site managers are allowed to add Service content items, but
also site contributors.

Let's logout and then login as 'contributor', a portal member that has the
contributor role assigned.

    >>> browser.getLink('Log out').click()
    >>> browser.open(portal_url + '/login_form')
    >>> browser.getControl(name='__ac_name').value = 'contributor'
    >>> browser.getControl(name='__ac_password').value = default_password
    >>> browser.getControl(name='submit').click()
    >>> browser.open(portal_url)

We use the 'Add new' menu to add a new content item.

    >>> browser.getLink('Add new').click()

We select 'Service' and click the 'Add' button to get to the add form.

    >>> browser.getControl('Service').click()
    >>> browser.getControl(name='form.button.Add').click()
    >>> 'Service' in browser.contents
    True

Now we fill the form and submit it.

    >>> browser.getControl(name='title').value = 'Service Sample'
    >>> browser.getControl('Save').click()
    >>> 'Changes saved' in browser.contents
    True

Done! We added a new Service content item logged in as contributor.

Finally, let's login back as manager.

    >>> browser.getLink('Log out').click()
    >>> browser.open(portal_url + '/login_form')
    >>> browser.getControl(name='__ac_name').value = portal_owner
    >>> browser.getControl(name='__ac_password').value = default_password
    >>> browser.getControl(name='submit').click()
    >>> browser.open(portal_url)



