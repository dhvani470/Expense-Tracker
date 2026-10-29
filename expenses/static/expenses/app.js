
/* ========================================
   EXPENSE TRACKER - JQUERY FEATURES
   ======================================== */

$(document).ready(function () {

    // FEATURE 1: Automatically dismiss Django messages.
    $('.alert[data-auto-dismiss="true"]').each(function () {
        const message = $(this);

        setTimeout(function () {
            message.stop(true, true).fadeOut(400, function () {
                $(this).remove();
            });
        }, 3000);
    });

    // Allow users to close messages immediately.
    $('.alert .btn-close').on('click', function () {
        $(this).closest('.alert').stop(true, true).fadeOut(250);
    });


    // FEATURE 2: Confirm before deleting an expense.
    $('form[data-confirm]').on('submit', function (event) {
        const message = $(this).attr('data-confirm');

        if (!window.confirm(message)) {
            event.preventDefault();
        }
    });


    // FEATURE 3: Validate the Add Expense form.
    $('form').has('#amount').on('submit', function (event) {
        const form = $(this);
        let isValid = true;

        // Remove errors from an earlier attempt.
        form.find('.jquery-error').remove();
        form.find('.is-invalid')
            .removeClass('is-invalid')
            .removeAttr('aria-invalid');

        // Check the amount.
        const amountValue = form.find('#amount').val().trim();
        const amount = Number(amountValue);

        if (amountValue === '' || !Number.isFinite(amount) || amount <= 0) {
            showError(
                form.find('#amount'),
                'Enter an amount greater than zero.'
            );
            isValid = false;
        }

        // Check the other required fields.
        const requiredFields = [
            { selector: '#category', message: 'Please select a category.' },
            { selector: '#date', message: 'Please select a date.' },
            { selector: '#description', message: 'Please enter a description.' },
            { selector: '#payment_method', message: 'Please select a payment method.' }
        ];

        requiredFields.forEach(function (field) {
            const input = form.find(field.selector);

            if (input.length && !String(input.val() || '').trim()) {
                showError(input, field.message);
                isValid = false;
            }
        });

        if (!isValid) {
            event.preventDefault();
        }
    });

    // Remove a field's error when the user corrects it.
    $('#amount, #category, #date, #description, #payment_method')
        .on('input change', function () {
            $(this)
                .removeClass('is-invalid')
                .removeAttr('aria-invalid');

            $(this)
                .next('.jquery-error')
                .remove();
        });


    // FEATURE 4: Reset Dashboard filters.
    $('[data-reset-filters]').on('click', function () {
        const form = $(this).closest('form');

        form.find('input').not(
            '[type="hidden"], [type="submit"], [type="button"], [name="csrfmiddlewaretoken"]'
        ).val('');

        form.find('select').prop('selectedIndex', 0);

        // Submit the cleared filters to refresh the results.
        form.trigger('submit');
    });


    // Helper: Display a validation message below a field.
    function showError(input, message) {
        input.addClass('is-invalid');
        input.attr('aria-invalid', 'true');

        $('<small>')
            .addClass('jquery-error text-danger d-block mt-1')
            .text(message)
            .insertAfter(input);
    }

});
