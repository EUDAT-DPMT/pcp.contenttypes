$(document).ready(function() {

    /* Perform some DOM modifications for the "Implementation Configuration" field
     * of RegisteredServiceComponent
     */

    $('#archetypes-fieldname-implementation_configuration #delete_all_entries').hide(); 
    $('#archetypes-fieldname-implementation_configuration #implementation_configuration_checkbox').hide(); 
    $('#archetypes-fieldname-implementation_configuration #delete_this_entry').hide(); 
    $('#archetypes-fieldname-implementation_configuration input[name="form.button.more"]').hide(); 
    $('#archetypes-fieldname-implementation_configuration input[type="checkbox"]').hide(); 
    $('#archetypes-fieldname-implementation_configuration input[name="implementation_configuration.key:records:ignore_empty"]').attr('readonly', 'readonly');

    $('head').append('<link href="https://fonts.googleapis.com/css?family=Raleway" rel="stylesheet">');
});
