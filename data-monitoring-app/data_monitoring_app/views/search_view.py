from django.shortcuts import render
from django.db import connection
from django.http import Http404

def view_and_search_tables(request):
    search_query = request.GET.get('search', '')
    tables = []

    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT table_schema, table_name
            FROM information_schema.tables
            WHERE table_type = 'BASE TABLE'
              AND table_schema NOT IN ('pg_catalog', 'information_schema')
            ORDER BY table_schema, table_name
        """)
        all_tables = [
            {'schema': row[0], 'table': row[1]}
            for row in cursor.fetchall()
        ]

        if search_query:
            tables = [
                t for t in all_tables
                if search_query.lower() in t['table'].lower()
            ]
        else:
            tables = all_tables

    table_count = len(tables)
    return render(request, 'search.html', {
        'tables': tables,
        'table_count': table_count,
        'search_query': search_query
    })

def view_table_data(request, schema, table):
    with connection.cursor() as cursor:
        try:
            cursor.execute(f'SELECT * FROM "{schema}"."{table}"')
            columns = [col[0] for col in cursor.description]
            rows = cursor.fetchall()
        except Exception:
            raise Http404("Table not found or inaccessible.")
    return render(request, 'table_data.html', {
        'table_name': f"{schema}.{table}",
        'columns': columns,
        'rows': rows,
    })

def search_view(request):
    return render(request, 'search.html')