def find_all_spectra(query_string, order_column, order_type, exact_match):
    """
    Return all spectra.
    Optional params:
    :param query_string : A querystring to match.
    :param order_column: Column to orderby.
    :param order_type: ASC or DESC.
    """
    spectra = SyntheticSpectra.objects.all()

    # Filter based on query string if provided
    if query_string:
        if exact_match == False:
            spectra = filter_spectra_include(spectra, query_string)
        else:
            spectra = filter_spectra_exact(spectra, query_string)

    # Order by column if provided
    if order_column:
        spectra = order_spectra(spectra, order_column, order_type)

    return list(spectra)