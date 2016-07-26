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
The RegisteredStorageResource content type
===============================

In this section we are tesing the RegisteredStorageResource content type by performing
basic operations like adding, updadating and deleting RegisteredStorageResource content
items.

Adding a new RegisteredStorageResource content item
--------------------------------

We use the 'Add new' menu to add a new content item.

    >>> browser.getLink('Add new').click()

Then we select the type of item we want to add. In this case we select
'RegisteredStorageResource' and click the 'Add' button to get to the add form.

    >>> browser.getControl('RegisteredStorageResource').click()
    >>> browser.getControl(name='form.button.Add').click()
    >>> 'RegisteredStorageResource' in browser.contents
    True

Now we fill the form and submit it.

    >>> browser.getControl(name='title').value = 'RegisteredStorageResource Sample'
    >>> browser.getControl('Save').click()
    >>> 'Changes saved' in browser.contents
    True

And we are done! We added a new 'RegisteredStorageResource' content item to the portal.

Updating an existing RegisteredStorageResource content item
---------------------------------------

Let's click on the 'edit' tab and update the object attribute values.

    >>> browser.getLink('Edit').click()
    >>> browser.getControl(name='title').value = 'New RegisteredStorageResource Sample'
    >>> browser.getControl('Save').click()

We check that the changes were applied.

    >>> 'Changes saved' in browser.contents
    True
    >>> 'New RegisteredStorageResource Sample' in browser.contents
    True

Removing a/an RegisteredStorageResource content item
--------------------------------

If we go to the home page, we can see a tab with the 'New RegisteredStorageResource
Sample' title in the global navigation tabs.

    >>> browser.open(portal_url)
    >>> 'New RegisteredStorageResource Sample' in browser.contents
    True

Now we are going to delete the 'New RegisteredStorageResource Sample' object. First we
go to the contents tab and select the 'New RegisteredStorageResource Sample' for
deletion.

    >>> browser.getLink('Contents').click()
    >>> browser.getControl('New RegisteredStorageResource Sample').click()

We click on the 'Delete' button.

    >>> browser.getControl('Delete').click()
    >>> 'Item(s) deleted' in browser.contents
    True

So, if we go back to the home page, there is no longer a 'New RegisteredStorageResource
Sample' tab.

    >>> browser.open(portal_url)
    >>> 'New RegisteredStorageResource Sample' in browser.contents
    False

Adding a new RegisteredStorageResource content item as contributor
------------------------------------------------

Not only site managers are allowed to add RegisteredStorageResource content items, but
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

We select 'RegisteredStorageResource' and click the 'Add' button to get to the add form.

    >>> browser.getControl('RegisteredStorageResource').click()
    >>> browser.getControl(name='form.button.Add').click()
    >>> 'RegisteredStorageResource' in browser.contents
    True

Now we fill the form and submit it.

    >>> browser.getControl(name='title').value = 'RegisteredStorageResource Sample'
    >>> browser.getControl('Save').click()
    >>> 'Changes saved' in browser.contents
    True

Done! We added a new RegisteredStorageResource content item logged in as contributor.

Finally, let's login back as manager.

    >>> browser.getLink('Log out').click()
    >>> browser.open(portal_url + '/login_form')
    >>> browser.getControl(name='__ac_name').value = portal_owner
    >>> browser.getControl(name='__ac_password').value = default_password
    >>> browser.getControl(name='submit').click()
    >>> browser.open(portal_url)


The RegisteredComputeResource content type
===============================

In this section we are tesing the RegisteredComputeResource content type by performing
basic operations like adding, updadating and deleting RegisteredComputeResource content
items.

Adding a new RegisteredComputeResource content item
--------------------------------

We use the 'Add new' menu to add a new content item.

    >>> browser.getLink('Add new').click()

Then we select the type of item we want to add. In this case we select
'RegisteredComputeResource' and click the 'Add' button to get to the add form.

    >>> browser.getControl('RegisteredComputeResource').click()
    >>> browser.getControl(name='form.button.Add').click()
    >>> 'RegisteredComputeResource' in browser.contents
    True

Now we fill the form and submit it.

    >>> browser.getControl(name='title').value = 'RegisteredComputeResource Sample'
    >>> browser.getControl('Save').click()
    >>> 'Changes saved' in browser.contents
    True

And we are done! We added a new 'RegisteredComputeResource' content item to the portal.

Updating an existing RegisteredComputeResource content item
---------------------------------------

Let's click on the 'edit' tab and update the object attribute values.

    >>> browser.getLink('Edit').click()
    >>> browser.getControl(name='title').value = 'New RegisteredComputeResource Sample'
    >>> browser.getControl('Save').click()

We check that the changes were applied.

    >>> 'Changes saved' in browser.contents
    True
    >>> 'New RegisteredComputeResource Sample' in browser.contents
    True

Removing a/an RegisteredComputeResource content item
--------------------------------

If we go to the home page, we can see a tab with the 'New RegisteredComputeResource
Sample' title in the global navigation tabs.

    >>> browser.open(portal_url)
    >>> 'New RegisteredComputeResource Sample' in browser.contents
    True

Now we are going to delete the 'New RegisteredComputeResource Sample' object. First we
go to the contents tab and select the 'New RegisteredComputeResource Sample' for
deletion.

    >>> browser.getLink('Contents').click()
    >>> browser.getControl('New RegisteredComputeResource Sample').click()

We click on the 'Delete' button.

    >>> browser.getControl('Delete').click()
    >>> 'Item(s) deleted' in browser.contents
    True

So, if we go back to the home page, there is no longer a 'New RegisteredComputeResource
Sample' tab.

    >>> browser.open(portal_url)
    >>> 'New RegisteredComputeResource Sample' in browser.contents
    False

Adding a new RegisteredComputeResource content item as contributor
------------------------------------------------

Not only site managers are allowed to add RegisteredComputeResource content items, but
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

We select 'RegisteredComputeResource' and click the 'Add' button to get to the add form.

    >>> browser.getControl('RegisteredComputeResource').click()
    >>> browser.getControl(name='form.button.Add').click()
    >>> 'RegisteredComputeResource' in browser.contents
    True

Now we fill the form and submit it.

    >>> browser.getControl(name='title').value = 'RegisteredComputeResource Sample'
    >>> browser.getControl('Save').click()
    >>> 'Changes saved' in browser.contents
    True

Done! We added a new RegisteredComputeResource content item logged in as contributor.

Finally, let's login back as manager.

    >>> browser.getLink('Log out').click()
    >>> browser.open(portal_url + '/login_form')
    >>> browser.getControl(name='__ac_name').value = portal_owner
    >>> browser.getControl(name='__ac_password').value = default_password
    >>> browser.getControl(name='submit').click()
    >>> browser.open(portal_url)


The ServiceOffer content type
===============================

In this section we are tesing the ServiceOffer content type by performing
basic operations like adding, updadating and deleting ServiceOffer content
items.

Adding a new ServiceOffer content item
--------------------------------

We use the 'Add new' menu to add a new content item.

    >>> browser.getLink('Add new').click()

Then we select the type of item we want to add. In this case we select
'ServiceOffer' and click the 'Add' button to get to the add form.

    >>> browser.getControl('ServiceOffer').click()
    >>> browser.getControl(name='form.button.Add').click()
    >>> 'ServiceOffer' in browser.contents
    True

Now we fill the form and submit it.

    >>> browser.getControl(name='title').value = 'ServiceOffer Sample'
    >>> browser.getControl('Save').click()
    >>> 'Changes saved' in browser.contents
    True

And we are done! We added a new 'ServiceOffer' content item to the portal.

Updating an existing ServiceOffer content item
---------------------------------------

Let's click on the 'edit' tab and update the object attribute values.

    >>> browser.getLink('Edit').click()
    >>> browser.getControl(name='title').value = 'New ServiceOffer Sample'
    >>> browser.getControl('Save').click()

We check that the changes were applied.

    >>> 'Changes saved' in browser.contents
    True
    >>> 'New ServiceOffer Sample' in browser.contents
    True

Removing a/an ServiceOffer content item
--------------------------------

If we go to the home page, we can see a tab with the 'New ServiceOffer
Sample' title in the global navigation tabs.

    >>> browser.open(portal_url)
    >>> 'New ServiceOffer Sample' in browser.contents
    True

Now we are going to delete the 'New ServiceOffer Sample' object. First we
go to the contents tab and select the 'New ServiceOffer Sample' for
deletion.

    >>> browser.getLink('Contents').click()
    >>> browser.getControl('New ServiceOffer Sample').click()

We click on the 'Delete' button.

    >>> browser.getControl('Delete').click()
    >>> 'Item(s) deleted' in browser.contents
    True

So, if we go back to the home page, there is no longer a 'New ServiceOffer
Sample' tab.

    >>> browser.open(portal_url)
    >>> 'New ServiceOffer Sample' in browser.contents
    False

Adding a new ServiceOffer content item as contributor
------------------------------------------------

Not only site managers are allowed to add ServiceOffer content items, but
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

We select 'ServiceOffer' and click the 'Add' button to get to the add form.

    >>> browser.getControl('ServiceOffer').click()
    >>> browser.getControl(name='form.button.Add').click()
    >>> 'ServiceOffer' in browser.contents
    True

Now we fill the form and submit it.

    >>> browser.getControl(name='title').value = 'ServiceOffer Sample'
    >>> browser.getControl('Save').click()
    >>> 'Changes saved' in browser.contents
    True

Done! We added a new ServiceOffer content item logged in as contributor.

Finally, let's login back as manager.

    >>> browser.getLink('Log out').click()
    >>> browser.open(portal_url + '/login_form')
    >>> browser.getControl(name='__ac_name').value = portal_owner
    >>> browser.getControl(name='__ac_password').value = default_password
    >>> browser.getControl(name='submit').click()
    >>> browser.open(portal_url)


The AccountingRecord content type
===============================

In this section we are tesing the AccountingRecord content type by performing
basic operations like adding, updadating and deleting AccountingRecord content
items.

Adding a new AccountingRecord content item
--------------------------------

We use the 'Add new' menu to add a new content item.

    >>> browser.getLink('Add new').click()

Then we select the type of item we want to add. In this case we select
'AccountingRecord' and click the 'Add' button to get to the add form.

    >>> browser.getControl('AccountingRecord').click()
    >>> browser.getControl(name='form.button.Add').click()
    >>> 'AccountingRecord' in browser.contents
    True

Now we fill the form and submit it.

    >>> browser.getControl(name='title').value = 'AccountingRecord Sample'
    >>> browser.getControl('Save').click()
    >>> 'Changes saved' in browser.contents
    True

And we are done! We added a new 'AccountingRecord' content item to the portal.

Updating an existing AccountingRecord content item
---------------------------------------

Let's click on the 'edit' tab and update the object attribute values.

    >>> browser.getLink('Edit').click()
    >>> browser.getControl(name='title').value = 'New AccountingRecord Sample'
    >>> browser.getControl('Save').click()

We check that the changes were applied.

    >>> 'Changes saved' in browser.contents
    True
    >>> 'New AccountingRecord Sample' in browser.contents
    True

Removing a/an AccountingRecord content item
--------------------------------

If we go to the home page, we can see a tab with the 'New AccountingRecord
Sample' title in the global navigation tabs.

    >>> browser.open(portal_url)
    >>> 'New AccountingRecord Sample' in browser.contents
    True

Now we are going to delete the 'New AccountingRecord Sample' object. First we
go to the contents tab and select the 'New AccountingRecord Sample' for
deletion.

    >>> browser.getLink('Contents').click()
    >>> browser.getControl('New AccountingRecord Sample').click()

We click on the 'Delete' button.

    >>> browser.getControl('Delete').click()
    >>> 'Item(s) deleted' in browser.contents
    True

So, if we go back to the home page, there is no longer a 'New AccountingRecord
Sample' tab.

    >>> browser.open(portal_url)
    >>> 'New AccountingRecord Sample' in browser.contents
    False

Adding a new AccountingRecord content item as contributor
------------------------------------------------

Not only site managers are allowed to add AccountingRecord content items, but
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

We select 'AccountingRecord' and click the 'Add' button to get to the add form.

    >>> browser.getControl('AccountingRecord').click()
    >>> browser.getControl(name='form.button.Add').click()
    >>> 'AccountingRecord' in browser.contents
    True

Now we fill the form and submit it.

    >>> browser.getControl(name='title').value = 'AccountingRecord Sample'
    >>> browser.getControl('Save').click()
    >>> 'Changes saved' in browser.contents
    True

Done! We added a new AccountingRecord content item logged in as contributor.

Finally, let's login back as manager.

    >>> browser.getLink('Log out').click()
    >>> browser.open(portal_url + '/login_form')
    >>> browser.getControl(name='__ac_name').value = portal_owner
    >>> browser.getControl(name='__ac_password').value = default_password
    >>> browser.getControl(name='submit').click()
    >>> browser.open(portal_url)


The Downtime content type
===============================

In this section we are tesing the Downtime content type by performing
basic operations like adding, updadating and deleting Downtime content
items.

Adding a new Downtime content item
--------------------------------

We use the 'Add new' menu to add a new content item.

    >>> browser.getLink('Add new').click()

Then we select the type of item we want to add. In this case we select
'Downtime' and click the 'Add' button to get to the add form.

    >>> browser.getControl('Downtime').click()
    >>> browser.getControl(name='form.button.Add').click()
    >>> 'Downtime' in browser.contents
    True

Now we fill the form and submit it.

    >>> browser.getControl(name='title').value = 'Downtime Sample'
    >>> browser.getControl('Save').click()
    >>> 'Changes saved' in browser.contents
    True

And we are done! We added a new 'Downtime' content item to the portal.

Updating an existing Downtime content item
---------------------------------------

Let's click on the 'edit' tab and update the object attribute values.

    >>> browser.getLink('Edit').click()
    >>> browser.getControl(name='title').value = 'New Downtime Sample'
    >>> browser.getControl('Save').click()

We check that the changes were applied.

    >>> 'Changes saved' in browser.contents
    True
    >>> 'New Downtime Sample' in browser.contents
    True

Removing a/an Downtime content item
--------------------------------

If we go to the home page, we can see a tab with the 'New Downtime
Sample' title in the global navigation tabs.

    >>> browser.open(portal_url)
    >>> 'New Downtime Sample' in browser.contents
    True

Now we are going to delete the 'New Downtime Sample' object. First we
go to the contents tab and select the 'New Downtime Sample' for
deletion.

    >>> browser.getLink('Contents').click()
    >>> browser.getControl('New Downtime Sample').click()

We click on the 'Delete' button.

    >>> browser.getControl('Delete').click()
    >>> 'Item(s) deleted' in browser.contents
    True

So, if we go back to the home page, there is no longer a 'New Downtime
Sample' tab.

    >>> browser.open(portal_url)
    >>> 'New Downtime Sample' in browser.contents
    False

Adding a new Downtime content item as contributor
------------------------------------------------

Not only site managers are allowed to add Downtime content items, but
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

We select 'Downtime' and click the 'Add' button to get to the add form.

    >>> browser.getControl('Downtime').click()
    >>> browser.getControl(name='form.button.Add').click()
    >>> 'Downtime' in browser.contents
    True

Now we fill the form and submit it.

    >>> browser.getControl(name='title').value = 'Downtime Sample'
    >>> browser.getControl('Save').click()
    >>> 'Changes saved' in browser.contents
    True

Done! We added a new Downtime content item logged in as contributor.

Finally, let's login back as manager.

    >>> browser.getLink('Log out').click()
    >>> browser.open(portal_url + '/login_form')
    >>> browser.getControl(name='__ac_name').value = portal_owner
    >>> browser.getControl(name='__ac_password').value = default_password
    >>> browser.getControl(name='submit').click()
    >>> browser.open(portal_url)


The ServiceComponentImplementationDetails content type
===============================

In this section we are tesing the ServiceComponentImplementationDetails content type by performing
basic operations like adding, updadating and deleting ServiceComponentImplementationDetails content
items.

Adding a new ServiceComponentImplementationDetails content item
--------------------------------

We use the 'Add new' menu to add a new content item.

    >>> browser.getLink('Add new').click()

Then we select the type of item we want to add. In this case we select
'ServiceComponentImplementationDetails' and click the 'Add' button to get to the add form.

    >>> browser.getControl('ServiceComponentImplementationDetails').click()
    >>> browser.getControl(name='form.button.Add').click()
    >>> 'ServiceComponentImplementationDetails' in browser.contents
    True

Now we fill the form and submit it.

    >>> browser.getControl(name='title').value = 'ServiceComponentImplementationDetails Sample'
    >>> browser.getControl('Save').click()
    >>> 'Changes saved' in browser.contents
    True

And we are done! We added a new 'ServiceComponentImplementationDetails' content item to the portal.

Updating an existing ServiceComponentImplementationDetails content item
---------------------------------------

Let's click on the 'edit' tab and update the object attribute values.

    >>> browser.getLink('Edit').click()
    >>> browser.getControl(name='title').value = 'New ServiceComponentImplementationDetails Sample'
    >>> browser.getControl('Save').click()

We check that the changes were applied.

    >>> 'Changes saved' in browser.contents
    True
    >>> 'New ServiceComponentImplementationDetails Sample' in browser.contents
    True

Removing a/an ServiceComponentImplementationDetails content item
--------------------------------

If we go to the home page, we can see a tab with the 'New ServiceComponentImplementationDetails
Sample' title in the global navigation tabs.

    >>> browser.open(portal_url)
    >>> 'New ServiceComponentImplementationDetails Sample' in browser.contents
    True

Now we are going to delete the 'New ServiceComponentImplementationDetails Sample' object. First we
go to the contents tab and select the 'New ServiceComponentImplementationDetails Sample' for
deletion.

    >>> browser.getLink('Contents').click()
    >>> browser.getControl('New ServiceComponentImplementationDetails Sample').click()

We click on the 'Delete' button.

    >>> browser.getControl('Delete').click()
    >>> 'Item(s) deleted' in browser.contents
    True

So, if we go back to the home page, there is no longer a 'New ServiceComponentImplementationDetails
Sample' tab.

    >>> browser.open(portal_url)
    >>> 'New ServiceComponentImplementationDetails Sample' in browser.contents
    False

Adding a new ServiceComponentImplementationDetails content item as contributor
------------------------------------------------

Not only site managers are allowed to add ServiceComponentImplementationDetails content items, but
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

We select 'ServiceComponentImplementationDetails' and click the 'Add' button to get to the add form.

    >>> browser.getControl('ServiceComponentImplementationDetails').click()
    >>> browser.getControl(name='form.button.Add').click()
    >>> 'ServiceComponentImplementationDetails' in browser.contents
    True

Now we fill the form and submit it.

    >>> browser.getControl(name='title').value = 'ServiceComponentImplementationDetails Sample'
    >>> browser.getControl('Save').click()
    >>> 'Changes saved' in browser.contents
    True

Done! We added a new ServiceComponentImplementationDetails content item logged in as contributor.

Finally, let's login back as manager.

    >>> browser.getLink('Log out').click()
    >>> browser.open(portal_url + '/login_form')
    >>> browser.getControl(name='__ac_name').value = portal_owner
    >>> browser.getControl(name='__ac_password').value = default_password
    >>> browser.getControl(name='submit').click()
    >>> browser.open(portal_url)


The ServiceComponentImplementation content type
===============================

In this section we are tesing the ServiceComponentImplementation content type by performing
basic operations like adding, updadating and deleting ServiceComponentImplementation content
items.

Adding a new ServiceComponentImplementation content item
--------------------------------

We use the 'Add new' menu to add a new content item.

    >>> browser.getLink('Add new').click()

Then we select the type of item we want to add. In this case we select
'ServiceComponentImplementation' and click the 'Add' button to get to the add form.

    >>> browser.getControl('ServiceComponentImplementation').click()
    >>> browser.getControl(name='form.button.Add').click()
    >>> 'ServiceComponentImplementation' in browser.contents
    True

Now we fill the form and submit it.

    >>> browser.getControl(name='title').value = 'ServiceComponentImplementation Sample'
    >>> browser.getControl('Save').click()
    >>> 'Changes saved' in browser.contents
    True

And we are done! We added a new 'ServiceComponentImplementation' content item to the portal.

Updating an existing ServiceComponentImplementation content item
---------------------------------------

Let's click on the 'edit' tab and update the object attribute values.

    >>> browser.getLink('Edit').click()
    >>> browser.getControl(name='title').value = 'New ServiceComponentImplementation Sample'
    >>> browser.getControl('Save').click()

We check that the changes were applied.

    >>> 'Changes saved' in browser.contents
    True
    >>> 'New ServiceComponentImplementation Sample' in browser.contents
    True

Removing a/an ServiceComponentImplementation content item
--------------------------------

If we go to the home page, we can see a tab with the 'New ServiceComponentImplementation
Sample' title in the global navigation tabs.

    >>> browser.open(portal_url)
    >>> 'New ServiceComponentImplementation Sample' in browser.contents
    True

Now we are going to delete the 'New ServiceComponentImplementation Sample' object. First we
go to the contents tab and select the 'New ServiceComponentImplementation Sample' for
deletion.

    >>> browser.getLink('Contents').click()
    >>> browser.getControl('New ServiceComponentImplementation Sample').click()

We click on the 'Delete' button.

    >>> browser.getControl('Delete').click()
    >>> 'Item(s) deleted' in browser.contents
    True

So, if we go back to the home page, there is no longer a 'New ServiceComponentImplementation
Sample' tab.

    >>> browser.open(portal_url)
    >>> 'New ServiceComponentImplementation Sample' in browser.contents
    False

Adding a new ServiceComponentImplementation content item as contributor
------------------------------------------------

Not only site managers are allowed to add ServiceComponentImplementation content items, but
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

We select 'ServiceComponentImplementation' and click the 'Add' button to get to the add form.

    >>> browser.getControl('ServiceComponentImplementation').click()
    >>> browser.getControl(name='form.button.Add').click()
    >>> 'ServiceComponentImplementation' in browser.contents
    True

Now we fill the form and submit it.

    >>> browser.getControl(name='title').value = 'ServiceComponentImplementation Sample'
    >>> browser.getControl('Save').click()
    >>> 'Changes saved' in browser.contents
    True

Done! We added a new ServiceComponentImplementation content item logged in as contributor.

Finally, let's login back as manager.

    >>> browser.getLink('Log out').click()
    >>> browser.open(portal_url + '/login_form')
    >>> browser.getControl(name='__ac_name').value = portal_owner
    >>> browser.getControl(name='__ac_password').value = default_password
    >>> browser.getControl(name='submit').click()
    >>> browser.open(portal_url)


The ServiceComponent content type
===============================

In this section we are tesing the ServiceComponent content type by performing
basic operations like adding, updadating and deleting ServiceComponent content
items.

Adding a new ServiceComponent content item
--------------------------------

We use the 'Add new' menu to add a new content item.

    >>> browser.getLink('Add new').click()

Then we select the type of item we want to add. In this case we select
'ServiceComponent' and click the 'Add' button to get to the add form.

    >>> browser.getControl('ServiceComponent').click()
    >>> browser.getControl(name='form.button.Add').click()
    >>> 'ServiceComponent' in browser.contents
    True

Now we fill the form and submit it.

    >>> browser.getControl(name='title').value = 'ServiceComponent Sample'
    >>> browser.getControl('Save').click()
    >>> 'Changes saved' in browser.contents
    True

And we are done! We added a new 'ServiceComponent' content item to the portal.

Updating an existing ServiceComponent content item
---------------------------------------

Let's click on the 'edit' tab and update the object attribute values.

    >>> browser.getLink('Edit').click()
    >>> browser.getControl(name='title').value = 'New ServiceComponent Sample'
    >>> browser.getControl('Save').click()

We check that the changes were applied.

    >>> 'Changes saved' in browser.contents
    True
    >>> 'New ServiceComponent Sample' in browser.contents
    True

Removing a/an ServiceComponent content item
--------------------------------

If we go to the home page, we can see a tab with the 'New ServiceComponent
Sample' title in the global navigation tabs.

    >>> browser.open(portal_url)
    >>> 'New ServiceComponent Sample' in browser.contents
    True

Now we are going to delete the 'New ServiceComponent Sample' object. First we
go to the contents tab and select the 'New ServiceComponent Sample' for
deletion.

    >>> browser.getLink('Contents').click()
    >>> browser.getControl('New ServiceComponent Sample').click()

We click on the 'Delete' button.

    >>> browser.getControl('Delete').click()
    >>> 'Item(s) deleted' in browser.contents
    True

So, if we go back to the home page, there is no longer a 'New ServiceComponent
Sample' tab.

    >>> browser.open(portal_url)
    >>> 'New ServiceComponent Sample' in browser.contents
    False

Adding a new ServiceComponent content item as contributor
------------------------------------------------

Not only site managers are allowed to add ServiceComponent content items, but
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

We select 'ServiceComponent' and click the 'Add' button to get to the add form.

    >>> browser.getControl('ServiceComponent').click()
    >>> browser.getControl(name='form.button.Add').click()
    >>> 'ServiceComponent' in browser.contents
    True

Now we fill the form and submit it.

    >>> browser.getControl(name='title').value = 'ServiceComponent Sample'
    >>> browser.getControl('Save').click()
    >>> 'Changes saved' in browser.contents
    True

Done! We added a new ServiceComponent content item logged in as contributor.

Finally, let's login back as manager.

    >>> browser.getLink('Log out').click()
    >>> browser.open(portal_url + '/login_form')
    >>> browser.getControl(name='__ac_name').value = portal_owner
    >>> browser.getControl(name='__ac_password').value = default_password
    >>> browser.getControl(name='submit').click()
    >>> browser.open(portal_url)


The Service Details content type
===============================

In this section we are tesing the Service Details content type by performing
basic operations like adding, updadating and deleting Service Details content
items.

Adding a new Service Details content item
--------------------------------

We use the 'Add new' menu to add a new content item.

    >>> browser.getLink('Add new').click()

Then we select the type of item we want to add. In this case we select
'Service Details' and click the 'Add' button to get to the add form.

    >>> browser.getControl('Service Details').click()
    >>> browser.getControl(name='form.button.Add').click()
    >>> 'Service Details' in browser.contents
    True

Now we fill the form and submit it.

    >>> browser.getControl(name='title').value = 'Service Details Sample'
    >>> browser.getControl('Save').click()
    >>> 'Changes saved' in browser.contents
    True

And we are done! We added a new 'Service Details' content item to the portal.

Updating an existing Service Details content item
---------------------------------------

Let's click on the 'edit' tab and update the object attribute values.

    >>> browser.getLink('Edit').click()
    >>> browser.getControl(name='title').value = 'New Service Details Sample'
    >>> browser.getControl('Save').click()

We check that the changes were applied.

    >>> 'Changes saved' in browser.contents
    True
    >>> 'New Service Details Sample' in browser.contents
    True

Removing a/an Service Details content item
--------------------------------

If we go to the home page, we can see a tab with the 'New Service Details
Sample' title in the global navigation tabs.

    >>> browser.open(portal_url)
    >>> 'New Service Details Sample' in browser.contents
    True

Now we are going to delete the 'New Service Details Sample' object. First we
go to the contents tab and select the 'New Service Details Sample' for
deletion.

    >>> browser.getLink('Contents').click()
    >>> browser.getControl('New Service Details Sample').click()

We click on the 'Delete' button.

    >>> browser.getControl('Delete').click()
    >>> 'Item(s) deleted' in browser.contents
    True

So, if we go back to the home page, there is no longer a 'New Service Details
Sample' tab.

    >>> browser.open(portal_url)
    >>> 'New Service Details Sample' in browser.contents
    False

Adding a new Service Details content item as contributor
------------------------------------------------

Not only site managers are allowed to add Service Details content items, but
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

We select 'Service Details' and click the 'Add' button to get to the add form.

    >>> browser.getControl('Service Details').click()
    >>> browser.getControl(name='form.button.Add').click()
    >>> 'Service Details' in browser.contents
    True

Now we fill the form and submit it.

    >>> browser.getControl(name='title').value = 'Service Details Sample'
    >>> browser.getControl('Save').click()
    >>> 'Changes saved' in browser.contents
    True

Done! We added a new Service Details content item logged in as contributor.

Finally, let's login back as manager.

    >>> browser.getLink('Log out').click()
    >>> browser.open(portal_url + '/login_form')
    >>> browser.getControl(name='__ac_name').value = portal_owner
    >>> browser.getControl(name='__ac_password').value = default_password
    >>> browser.getControl(name='submit').click()
    >>> browser.open(portal_url)


The RegisteredResource content type
===============================

In this section we are tesing the RegisteredResource content type by performing
basic operations like adding, updadating and deleting RegisteredResource content
items.

Adding a new RegisteredResource content item
--------------------------------

We use the 'Add new' menu to add a new content item.

    >>> browser.getLink('Add new').click()

Then we select the type of item we want to add. In this case we select
'RegisteredResource' and click the 'Add' button to get to the add form.

    >>> browser.getControl('RegisteredResource').click()
    >>> browser.getControl(name='form.button.Add').click()
    >>> 'RegisteredResource' in browser.contents
    True

Now we fill the form and submit it.

    >>> browser.getControl(name='title').value = 'RegisteredResource Sample'
    >>> browser.getControl('Save').click()
    >>> 'Changes saved' in browser.contents
    True

And we are done! We added a new 'RegisteredResource' content item to the portal.

Updating an existing RegisteredResource content item
---------------------------------------

Let's click on the 'edit' tab and update the object attribute values.

    >>> browser.getLink('Edit').click()
    >>> browser.getControl(name='title').value = 'New RegisteredResource Sample'
    >>> browser.getControl('Save').click()

We check that the changes were applied.

    >>> 'Changes saved' in browser.contents
    True
    >>> 'New RegisteredResource Sample' in browser.contents
    True

Removing a/an RegisteredResource content item
--------------------------------

If we go to the home page, we can see a tab with the 'New RegisteredResource
Sample' title in the global navigation tabs.

    >>> browser.open(portal_url)
    >>> 'New RegisteredResource Sample' in browser.contents
    True

Now we are going to delete the 'New RegisteredResource Sample' object. First we
go to the contents tab and select the 'New RegisteredResource Sample' for
deletion.

    >>> browser.getLink('Contents').click()
    >>> browser.getControl('New RegisteredResource Sample').click()

We click on the 'Delete' button.

    >>> browser.getControl('Delete').click()
    >>> 'Item(s) deleted' in browser.contents
    True

So, if we go back to the home page, there is no longer a 'New RegisteredResource
Sample' tab.

    >>> browser.open(portal_url)
    >>> 'New RegisteredResource Sample' in browser.contents
    False

Adding a new RegisteredResource content item as contributor
------------------------------------------------

Not only site managers are allowed to add RegisteredResource content items, but
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

We select 'RegisteredResource' and click the 'Add' button to get to the add form.

    >>> browser.getControl('RegisteredResource').click()
    >>> browser.getControl(name='form.button.Add').click()
    >>> 'RegisteredResource' in browser.contents
    True

Now we fill the form and submit it.

    >>> browser.getControl(name='title').value = 'RegisteredResource Sample'
    >>> browser.getControl('Save').click()
    >>> 'Changes saved' in browser.contents
    True

Done! We added a new RegisteredResource content item logged in as contributor.

Finally, let's login back as manager.

    >>> browser.getLink('Log out').click()
    >>> browser.open(portal_url + '/login_form')
    >>> browser.getControl(name='__ac_name').value = portal_owner
    >>> browser.getControl(name='__ac_password').value = default_password
    >>> browser.getControl(name='submit').click()
    >>> browser.open(portal_url)


The RegisteredServiceComponent content type
===============================

In this section we are tesing the RegisteredServiceComponent content type by performing
basic operations like adding, updadating and deleting RegisteredServiceComponent content
items.

Adding a new RegisteredServiceComponent content item
--------------------------------

We use the 'Add new' menu to add a new content item.

    >>> browser.getLink('Add new').click()

Then we select the type of item we want to add. In this case we select
'RegisteredServiceComponent' and click the 'Add' button to get to the add form.

    >>> browser.getControl('RegisteredServiceComponent').click()
    >>> browser.getControl(name='form.button.Add').click()
    >>> 'RegisteredServiceComponent' in browser.contents
    True

Now we fill the form and submit it.

    >>> browser.getControl(name='title').value = 'RegisteredServiceComponent Sample'
    >>> browser.getControl('Save').click()
    >>> 'Changes saved' in browser.contents
    True

And we are done! We added a new 'RegisteredServiceComponent' content item to the portal.

Updating an existing RegisteredServiceComponent content item
---------------------------------------

Let's click on the 'edit' tab and update the object attribute values.

    >>> browser.getLink('Edit').click()
    >>> browser.getControl(name='title').value = 'New RegisteredServiceComponent Sample'
    >>> browser.getControl('Save').click()

We check that the changes were applied.

    >>> 'Changes saved' in browser.contents
    True
    >>> 'New RegisteredServiceComponent Sample' in browser.contents
    True

Removing a/an RegisteredServiceComponent content item
--------------------------------

If we go to the home page, we can see a tab with the 'New RegisteredServiceComponent
Sample' title in the global navigation tabs.

    >>> browser.open(portal_url)
    >>> 'New RegisteredServiceComponent Sample' in browser.contents
    True

Now we are going to delete the 'New RegisteredServiceComponent Sample' object. First we
go to the contents tab and select the 'New RegisteredServiceComponent Sample' for
deletion.

    >>> browser.getLink('Contents').click()
    >>> browser.getControl('New RegisteredServiceComponent Sample').click()

We click on the 'Delete' button.

    >>> browser.getControl('Delete').click()
    >>> 'Item(s) deleted' in browser.contents
    True

So, if we go back to the home page, there is no longer a 'New RegisteredServiceComponent
Sample' tab.

    >>> browser.open(portal_url)
    >>> 'New RegisteredServiceComponent Sample' in browser.contents
    False

Adding a new RegisteredServiceComponent content item as contributor
------------------------------------------------

Not only site managers are allowed to add RegisteredServiceComponent content items, but
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

We select 'RegisteredServiceComponent' and click the 'Add' button to get to the add form.

    >>> browser.getControl('RegisteredServiceComponent').click()
    >>> browser.getControl(name='form.button.Add').click()
    >>> 'RegisteredServiceComponent' in browser.contents
    True

Now we fill the form and submit it.

    >>> browser.getControl(name='title').value = 'RegisteredServiceComponent Sample'
    >>> browser.getControl('Save').click()
    >>> 'Changes saved' in browser.contents
    True

Done! We added a new RegisteredServiceComponent content item logged in as contributor.

Finally, let's login back as manager.

    >>> browser.getLink('Log out').click()
    >>> browser.open(portal_url + '/login_form')
    >>> browser.getControl(name='__ac_name').value = portal_owner
    >>> browser.getControl(name='__ac_password').value = default_password
    >>> browser.getControl(name='submit').click()
    >>> browser.open(portal_url)


The RegisteredService content type
===============================

In this section we are tesing the RegisteredService content type by performing
basic operations like adding, updadating and deleting RegisteredService content
items.

Adding a new RegisteredService content item
--------------------------------

We use the 'Add new' menu to add a new content item.

    >>> browser.getLink('Add new').click()

Then we select the type of item we want to add. In this case we select
'RegisteredService' and click the 'Add' button to get to the add form.

    >>> browser.getControl('RegisteredService').click()
    >>> browser.getControl(name='form.button.Add').click()
    >>> 'RegisteredService' in browser.contents
    True

Now we fill the form and submit it.

    >>> browser.getControl(name='title').value = 'RegisteredService Sample'
    >>> browser.getControl('Save').click()
    >>> 'Changes saved' in browser.contents
    True

And we are done! We added a new 'RegisteredService' content item to the portal.

Updating an existing RegisteredService content item
---------------------------------------

Let's click on the 'edit' tab and update the object attribute values.

    >>> browser.getLink('Edit').click()
    >>> browser.getControl(name='title').value = 'New RegisteredService Sample'
    >>> browser.getControl('Save').click()

We check that the changes were applied.

    >>> 'Changes saved' in browser.contents
    True
    >>> 'New RegisteredService Sample' in browser.contents
    True

Removing a/an RegisteredService content item
--------------------------------

If we go to the home page, we can see a tab with the 'New RegisteredService
Sample' title in the global navigation tabs.

    >>> browser.open(portal_url)
    >>> 'New RegisteredService Sample' in browser.contents
    True

Now we are going to delete the 'New RegisteredService Sample' object. First we
go to the contents tab and select the 'New RegisteredService Sample' for
deletion.

    >>> browser.getLink('Contents').click()
    >>> browser.getControl('New RegisteredService Sample').click()

We click on the 'Delete' button.

    >>> browser.getControl('Delete').click()
    >>> 'Item(s) deleted' in browser.contents
    True

So, if we go back to the home page, there is no longer a 'New RegisteredService
Sample' tab.

    >>> browser.open(portal_url)
    >>> 'New RegisteredService Sample' in browser.contents
    False

Adding a new RegisteredService content item as contributor
------------------------------------------------

Not only site managers are allowed to add RegisteredService content items, but
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

We select 'RegisteredService' and click the 'Add' button to get to the add form.

    >>> browser.getControl('RegisteredService').click()
    >>> browser.getControl(name='form.button.Add').click()
    >>> 'RegisteredService' in browser.contents
    True

Now we fill the form and submit it.

    >>> browser.getControl(name='title').value = 'RegisteredService Sample'
    >>> browser.getControl('Save').click()
    >>> 'Changes saved' in browser.contents
    True

Done! We added a new RegisteredService content item logged in as contributor.

Finally, let's login back as manager.

    >>> browser.getLink('Log out').click()
    >>> browser.open(portal_url + '/login_form')
    >>> browser.getControl(name='__ac_name').value = portal_owner
    >>> browser.getControl(name='__ac_password').value = default_password
    >>> browser.getControl(name='submit').click()
    >>> browser.open(portal_url)


The ResourceRequest content type
===============================

In this section we are tesing the ResourceRequest content type by performing
basic operations like adding, updadating and deleting ResourceRequest content
items.

Adding a new ResourceRequest content item
--------------------------------

We use the 'Add new' menu to add a new content item.

    >>> browser.getLink('Add new').click()

Then we select the type of item we want to add. In this case we select
'ResourceRequest' and click the 'Add' button to get to the add form.

    >>> browser.getControl('ResourceRequest').click()
    >>> browser.getControl(name='form.button.Add').click()
    >>> 'ResourceRequest' in browser.contents
    True

Now we fill the form and submit it.

    >>> browser.getControl(name='title').value = 'ResourceRequest Sample'
    >>> browser.getControl('Save').click()
    >>> 'Changes saved' in browser.contents
    True

And we are done! We added a new 'ResourceRequest' content item to the portal.

Updating an existing ResourceRequest content item
---------------------------------------

Let's click on the 'edit' tab and update the object attribute values.

    >>> browser.getLink('Edit').click()
    >>> browser.getControl(name='title').value = 'New ResourceRequest Sample'
    >>> browser.getControl('Save').click()

We check that the changes were applied.

    >>> 'Changes saved' in browser.contents
    True
    >>> 'New ResourceRequest Sample' in browser.contents
    True

Removing a/an ResourceRequest content item
--------------------------------

If we go to the home page, we can see a tab with the 'New ResourceRequest
Sample' title in the global navigation tabs.

    >>> browser.open(portal_url)
    >>> 'New ResourceRequest Sample' in browser.contents
    True

Now we are going to delete the 'New ResourceRequest Sample' object. First we
go to the contents tab and select the 'New ResourceRequest Sample' for
deletion.

    >>> browser.getLink('Contents').click()
    >>> browser.getControl('New ResourceRequest Sample').click()

We click on the 'Delete' button.

    >>> browser.getControl('Delete').click()
    >>> 'Item(s) deleted' in browser.contents
    True

So, if we go back to the home page, there is no longer a 'New ResourceRequest
Sample' tab.

    >>> browser.open(portal_url)
    >>> 'New ResourceRequest Sample' in browser.contents
    False

Adding a new ResourceRequest content item as contributor
------------------------------------------------

Not only site managers are allowed to add ResourceRequest content items, but
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

We select 'ResourceRequest' and click the 'Add' button to get to the add form.

    >>> browser.getControl('ResourceRequest').click()
    >>> browser.getControl(name='form.button.Add').click()
    >>> 'ResourceRequest' in browser.contents
    True

Now we fill the form and submit it.

    >>> browser.getControl(name='title').value = 'ResourceRequest Sample'
    >>> browser.getControl('Save').click()
    >>> 'Changes saved' in browser.contents
    True

Done! We added a new ResourceRequest content item logged in as contributor.

Finally, let's login back as manager.

    >>> browser.getLink('Log out').click()
    >>> browser.open(portal_url + '/login_form')
    >>> browser.getControl(name='__ac_name').value = portal_owner
    >>> browser.getControl(name='__ac_password').value = default_password
    >>> browser.getControl(name='submit').click()
    >>> browser.open(portal_url)


The ServiceComponentRequest content type
===============================

In this section we are tesing the ServiceComponentRequest content type by performing
basic operations like adding, updadating and deleting ServiceComponentRequest content
items.

Adding a new ServiceComponentRequest content item
--------------------------------

We use the 'Add new' menu to add a new content item.

    >>> browser.getLink('Add new').click()

Then we select the type of item we want to add. In this case we select
'ServiceComponentRequest' and click the 'Add' button to get to the add form.

    >>> browser.getControl('ServiceComponentRequest').click()
    >>> browser.getControl(name='form.button.Add').click()
    >>> 'ServiceComponentRequest' in browser.contents
    True

Now we fill the form and submit it.

    >>> browser.getControl(name='title').value = 'ServiceComponentRequest Sample'
    >>> browser.getControl('Save').click()
    >>> 'Changes saved' in browser.contents
    True

And we are done! We added a new 'ServiceComponentRequest' content item to the portal.

Updating an existing ServiceComponentRequest content item
---------------------------------------

Let's click on the 'edit' tab and update the object attribute values.

    >>> browser.getLink('Edit').click()
    >>> browser.getControl(name='title').value = 'New ServiceComponentRequest Sample'
    >>> browser.getControl('Save').click()

We check that the changes were applied.

    >>> 'Changes saved' in browser.contents
    True
    >>> 'New ServiceComponentRequest Sample' in browser.contents
    True

Removing a/an ServiceComponentRequest content item
--------------------------------

If we go to the home page, we can see a tab with the 'New ServiceComponentRequest
Sample' title in the global navigation tabs.

    >>> browser.open(portal_url)
    >>> 'New ServiceComponentRequest Sample' in browser.contents
    True

Now we are going to delete the 'New ServiceComponentRequest Sample' object. First we
go to the contents tab and select the 'New ServiceComponentRequest Sample' for
deletion.

    >>> browser.getLink('Contents').click()
    >>> browser.getControl('New ServiceComponentRequest Sample').click()

We click on the 'Delete' button.

    >>> browser.getControl('Delete').click()
    >>> 'Item(s) deleted' in browser.contents
    True

So, if we go back to the home page, there is no longer a 'New ServiceComponentRequest
Sample' tab.

    >>> browser.open(portal_url)
    >>> 'New ServiceComponentRequest Sample' in browser.contents
    False

Adding a new ServiceComponentRequest content item as contributor
------------------------------------------------

Not only site managers are allowed to add ServiceComponentRequest content items, but
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

We select 'ServiceComponentRequest' and click the 'Add' button to get to the add form.

    >>> browser.getControl('ServiceComponentRequest').click()
    >>> browser.getControl(name='form.button.Add').click()
    >>> 'ServiceComponentRequest' in browser.contents
    True

Now we fill the form and submit it.

    >>> browser.getControl(name='title').value = 'ServiceComponentRequest Sample'
    >>> browser.getControl('Save').click()
    >>> 'Changes saved' in browser.contents
    True

Done! We added a new ServiceComponentRequest content item logged in as contributor.

Finally, let's login back as manager.

    >>> browser.getLink('Log out').click()
    >>> browser.open(portal_url + '/login_form')
    >>> browser.getControl(name='__ac_name').value = portal_owner
    >>> browser.getControl(name='__ac_password').value = default_password
    >>> browser.getControl(name='submit').click()
    >>> browser.open(portal_url)


The ServiceRequest content type
===============================

In this section we are tesing the ServiceRequest content type by performing
basic operations like adding, updadating and deleting ServiceRequest content
items.

Adding a new ServiceRequest content item
--------------------------------

We use the 'Add new' menu to add a new content item.

    >>> browser.getLink('Add new').click()

Then we select the type of item we want to add. In this case we select
'ServiceRequest' and click the 'Add' button to get to the add form.

    >>> browser.getControl('ServiceRequest').click()
    >>> browser.getControl(name='form.button.Add').click()
    >>> 'ServiceRequest' in browser.contents
    True

Now we fill the form and submit it.

    >>> browser.getControl(name='title').value = 'ServiceRequest Sample'
    >>> browser.getControl('Save').click()
    >>> 'Changes saved' in browser.contents
    True

And we are done! We added a new 'ServiceRequest' content item to the portal.

Updating an existing ServiceRequest content item
---------------------------------------

Let's click on the 'edit' tab and update the object attribute values.

    >>> browser.getLink('Edit').click()
    >>> browser.getControl(name='title').value = 'New ServiceRequest Sample'
    >>> browser.getControl('Save').click()

We check that the changes were applied.

    >>> 'Changes saved' in browser.contents
    True
    >>> 'New ServiceRequest Sample' in browser.contents
    True

Removing a/an ServiceRequest content item
--------------------------------

If we go to the home page, we can see a tab with the 'New ServiceRequest
Sample' title in the global navigation tabs.

    >>> browser.open(portal_url)
    >>> 'New ServiceRequest Sample' in browser.contents
    True

Now we are going to delete the 'New ServiceRequest Sample' object. First we
go to the contents tab and select the 'New ServiceRequest Sample' for
deletion.

    >>> browser.getLink('Contents').click()
    >>> browser.getControl('New ServiceRequest Sample').click()

We click on the 'Delete' button.

    >>> browser.getControl('Delete').click()
    >>> 'Item(s) deleted' in browser.contents
    True

So, if we go back to the home page, there is no longer a 'New ServiceRequest
Sample' tab.

    >>> browser.open(portal_url)
    >>> 'New ServiceRequest Sample' in browser.contents
    False

Adding a new ServiceRequest content item as contributor
------------------------------------------------

Not only site managers are allowed to add ServiceRequest content items, but
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

We select 'ServiceRequest' and click the 'Add' button to get to the add form.

    >>> browser.getControl('ServiceRequest').click()
    >>> browser.getControl(name='form.button.Add').click()
    >>> 'ServiceRequest' in browser.contents
    True

Now we fill the form and submit it.

    >>> browser.getControl(name='title').value = 'ServiceRequest Sample'
    >>> browser.getControl('Save').click()
    >>> 'Changes saved' in browser.contents
    True

Done! We added a new ServiceRequest content item logged in as contributor.

Finally, let's login back as manager.

    >>> browser.getLink('Log out').click()
    >>> browser.open(portal_url + '/login_form')
    >>> browser.getControl(name='__ac_name').value = portal_owner
    >>> browser.getControl(name='__ac_password').value = default_password
    >>> browser.getControl(name='submit').click()
    >>> browser.open(portal_url)


The ServiceComponentOffer content type
===============================

In this section we are tesing the ServiceComponentOffer content type by performing
basic operations like adding, updadating and deleting ServiceComponentOffer content
items.

Adding a new ServiceComponentOffer content item
--------------------------------

We use the 'Add new' menu to add a new content item.

    >>> browser.getLink('Add new').click()

Then we select the type of item we want to add. In this case we select
'ServiceComponentOffer' and click the 'Add' button to get to the add form.

    >>> browser.getControl('ServiceComponentOffer').click()
    >>> browser.getControl(name='form.button.Add').click()
    >>> 'ServiceComponentOffer' in browser.contents
    True

Now we fill the form and submit it.

    >>> browser.getControl(name='title').value = 'ServiceComponentOffer Sample'
    >>> browser.getControl('Save').click()
    >>> 'Changes saved' in browser.contents
    True

And we are done! We added a new 'ServiceComponentOffer' content item to the portal.

Updating an existing ServiceComponentOffer content item
---------------------------------------

Let's click on the 'edit' tab and update the object attribute values.

    >>> browser.getLink('Edit').click()
    >>> browser.getControl(name='title').value = 'New ServiceComponentOffer Sample'
    >>> browser.getControl('Save').click()

We check that the changes were applied.

    >>> 'Changes saved' in browser.contents
    True
    >>> 'New ServiceComponentOffer Sample' in browser.contents
    True

Removing a/an ServiceComponentOffer content item
--------------------------------

If we go to the home page, we can see a tab with the 'New ServiceComponentOffer
Sample' title in the global navigation tabs.

    >>> browser.open(portal_url)
    >>> 'New ServiceComponentOffer Sample' in browser.contents
    True

Now we are going to delete the 'New ServiceComponentOffer Sample' object. First we
go to the contents tab and select the 'New ServiceComponentOffer Sample' for
deletion.

    >>> browser.getLink('Contents').click()
    >>> browser.getControl('New ServiceComponentOffer Sample').click()

We click on the 'Delete' button.

    >>> browser.getControl('Delete').click()
    >>> 'Item(s) deleted' in browser.contents
    True

So, if we go back to the home page, there is no longer a 'New ServiceComponentOffer
Sample' tab.

    >>> browser.open(portal_url)
    >>> 'New ServiceComponentOffer Sample' in browser.contents
    False

Adding a new ServiceComponentOffer content item as contributor
------------------------------------------------

Not only site managers are allowed to add ServiceComponentOffer content items, but
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

We select 'ServiceComponentOffer' and click the 'Add' button to get to the add form.

    >>> browser.getControl('ServiceComponentOffer').click()
    >>> browser.getControl(name='form.button.Add').click()
    >>> 'ServiceComponentOffer' in browser.contents
    True

Now we fill the form and submit it.

    >>> browser.getControl(name='title').value = 'ServiceComponentOffer Sample'
    >>> browser.getControl('Save').click()
    >>> 'Changes saved' in browser.contents
    True

Done! We added a new ServiceComponentOffer content item logged in as contributor.

Finally, let's login back as manager.

    >>> browser.getLink('Log out').click()
    >>> browser.open(portal_url + '/login_form')
    >>> browser.getControl(name='__ac_name').value = portal_owner
    >>> browser.getControl(name='__ac_password').value = default_password
    >>> browser.getControl(name='submit').click()
    >>> browser.open(portal_url)


The ResourceOffer content type
===============================

In this section we are tesing the ResourceOffer content type by performing
basic operations like adding, updadating and deleting ResourceOffer content
items.

Adding a new ResourceOffer content item
--------------------------------

We use the 'Add new' menu to add a new content item.

    >>> browser.getLink('Add new').click()

Then we select the type of item we want to add. In this case we select
'ResourceOffer' and click the 'Add' button to get to the add form.

    >>> browser.getControl('ResourceOffer').click()
    >>> browser.getControl(name='form.button.Add').click()
    >>> 'ResourceOffer' in browser.contents
    True

Now we fill the form and submit it.

    >>> browser.getControl(name='title').value = 'ResourceOffer Sample'
    >>> browser.getControl('Save').click()
    >>> 'Changes saved' in browser.contents
    True

And we are done! We added a new 'ResourceOffer' content item to the portal.

Updating an existing ResourceOffer content item
---------------------------------------

Let's click on the 'edit' tab and update the object attribute values.

    >>> browser.getLink('Edit').click()
    >>> browser.getControl(name='title').value = 'New ResourceOffer Sample'
    >>> browser.getControl('Save').click()

We check that the changes were applied.

    >>> 'Changes saved' in browser.contents
    True
    >>> 'New ResourceOffer Sample' in browser.contents
    True

Removing a/an ResourceOffer content item
--------------------------------

If we go to the home page, we can see a tab with the 'New ResourceOffer
Sample' title in the global navigation tabs.

    >>> browser.open(portal_url)
    >>> 'New ResourceOffer Sample' in browser.contents
    True

Now we are going to delete the 'New ResourceOffer Sample' object. First we
go to the contents tab and select the 'New ResourceOffer Sample' for
deletion.

    >>> browser.getLink('Contents').click()
    >>> browser.getControl('New ResourceOffer Sample').click()

We click on the 'Delete' button.

    >>> browser.getControl('Delete').click()
    >>> 'Item(s) deleted' in browser.contents
    True

So, if we go back to the home page, there is no longer a 'New ResourceOffer
Sample' tab.

    >>> browser.open(portal_url)
    >>> 'New ResourceOffer Sample' in browser.contents
    False

Adding a new ResourceOffer content item as contributor
------------------------------------------------

Not only site managers are allowed to add ResourceOffer content items, but
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

We select 'ResourceOffer' and click the 'Add' button to get to the add form.

    >>> browser.getControl('ResourceOffer').click()
    >>> browser.getControl(name='form.button.Add').click()
    >>> 'ResourceOffer' in browser.contents
    True

Now we fill the form and submit it.

    >>> browser.getControl(name='title').value = 'ResourceOffer Sample'
    >>> browser.getControl('Save').click()
    >>> 'Changes saved' in browser.contents
    True

Done! We added a new ResourceOffer content item logged in as contributor.

Finally, let's login back as manager.

    >>> browser.getLink('Log out').click()
    >>> browser.open(portal_url + '/login_form')
    >>> browser.getControl(name='__ac_name').value = portal_owner
    >>> browser.getControl(name='__ac_password').value = default_password
    >>> browser.getControl(name='submit').click()
    >>> browser.open(portal_url)


The Plan content type
===============================

In this section we are tesing the Plan content type by performing
basic operations like adding, updadating and deleting Plan content
items.

Adding a new Plan content item
--------------------------------

We use the 'Add new' menu to add a new content item.

    >>> browser.getLink('Add new').click()

Then we select the type of item we want to add. In this case we select
'Plan' and click the 'Add' button to get to the add form.

    >>> browser.getControl('Plan').click()
    >>> browser.getControl(name='form.button.Add').click()
    >>> 'Plan' in browser.contents
    True

Now we fill the form and submit it.

    >>> browser.getControl(name='title').value = 'Plan Sample'
    >>> browser.getControl('Save').click()
    >>> 'Changes saved' in browser.contents
    True

And we are done! We added a new 'Plan' content item to the portal.

Updating an existing Plan content item
---------------------------------------

Let's click on the 'edit' tab and update the object attribute values.

    >>> browser.getLink('Edit').click()
    >>> browser.getControl(name='title').value = 'New Plan Sample'
    >>> browser.getControl('Save').click()

We check that the changes were applied.

    >>> 'Changes saved' in browser.contents
    True
    >>> 'New Plan Sample' in browser.contents
    True

Removing a/an Plan content item
--------------------------------

If we go to the home page, we can see a tab with the 'New Plan
Sample' title in the global navigation tabs.

    >>> browser.open(portal_url)
    >>> 'New Plan Sample' in browser.contents
    True

Now we are going to delete the 'New Plan Sample' object. First we
go to the contents tab and select the 'New Plan Sample' for
deletion.

    >>> browser.getLink('Contents').click()
    >>> browser.getControl('New Plan Sample').click()

We click on the 'Delete' button.

    >>> browser.getControl('Delete').click()
    >>> 'Item(s) deleted' in browser.contents
    True

So, if we go back to the home page, there is no longer a 'New Plan
Sample' tab.

    >>> browser.open(portal_url)
    >>> 'New Plan Sample' in browser.contents
    False

Adding a new Plan content item as contributor
------------------------------------------------

Not only site managers are allowed to add Plan content items, but
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

We select 'Plan' and click the 'Add' button to get to the add form.

    >>> browser.getControl('Plan').click()
    >>> browser.getControl(name='form.button.Add').click()
    >>> 'Plan' in browser.contents
    True

Now we fill the form and submit it.

    >>> browser.getControl(name='title').value = 'Plan Sample'
    >>> browser.getControl('Save').click()
    >>> 'Changes saved' in browser.contents
    True

Done! We added a new Plan content item logged in as contributor.

Finally, let's login back as manager.

    >>> browser.getLink('Log out').click()
    >>> browser.open(portal_url + '/login_form')
    >>> browser.getControl(name='__ac_name').value = portal_owner
    >>> browser.getControl(name='__ac_password').value = default_password
    >>> browser.getControl(name='submit').click()
    >>> browser.open(portal_url)


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



