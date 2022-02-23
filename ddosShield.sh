NO_OF_CONNECTIONS=150
daemon_running=0

# Check active connections and ban if neccessary.
check_connections()
{
    TMP_PREFIX='TEMP'
    TMP_FILE="mktemp ./$TMP_PREFIX.XXXXXXXX"
    BAD_IP_LIST=$($TMP_FILE)
    
    ban_only_incoming "$BAD_IP_LIST"

    FOUND=$(cat "$BAD_IP_LIST")
} 

ban_only_incoming()
{
    ALL_CONNS=$(mktemp "$TMP_PREFIX".XXXXXXXX)

    # Find all connections
    get_connections | \
        # Extract both local and foreign address:port
        awk '{print $5" "$6;}' > \
        "$ALL_CONNS"

    awk '
    FNR == 1 { ++fIndex }
    fIndex == 1{ip_list[$1];next}
    fIndex == 2{ip6_list[$1];next}
    {
        ip_pos = index($0, "0.0.0.0");
        ip6_pos = index($0, "[::]");
        if (ip_pos != 0) {
            port_pos = index($0, ":");
            print $0;
            for (ip in ip_list){
                print ip substr($0, port_pos);
            }
        } else if (ip6_pos != 0) {
            port_pos = index($0, "]:");
            print $0;
            for (ip in ip6_list){
                print "[" ip substr($0, port_pos);
            }
        } else {
            print $0;
        }
    }
    ' "$ALL_SERVER_IP" "$ALL_SERVER_IP6" "$ALL_LISTENING" > "$ALL_LISTENING_FULL"

    # Only keep connections which are connected to local listening service
    awk 'NR==FNR{a[$1];next} $1 in a {print $2}' "$ALL_LISTENING_FULL" "$ALL_CONNS" | \
        # Strip port and [ ] brackets
        sed -E "s/\\[//g; s/\\]//g; s/:[0-9]+$//g" | \
        # Only leave non whitelisted, we add ::1 to ensure -v works
        grepcidr -v -e "$SERVER_IP_LIST $whitelist ::1" 2>/dev/null | \
        # Sort addresses for uniq to work correctly
        sort | \
        # Group same occurrences of ip and prepend amount of occurences found
        uniq -c | \
        # Numerical sort in reverse order
        sort -nr | \
        # Only store connections that exceed max allowed
        awk "{ if (\$1 >= $NO_OF_CONNECTIONS) print; }" > \
        "$1"

    # remove temp files
    rm "$ALL_LISTENING" "$ALL_LISTENING_FULL" "$ALL_CONNS" \
        "$ALL_SERVER_IP" "$ALL_SERVER_IP6"
}

get_connections()
{
    ss -ntu"$1" \
        state $(echo "$CONN_STATES" | sed 's/:/ state /g') | \
        # fixing dependency on '-H' switch which is unavailable in some versions of ss
        tail -n +2 | \
        # Fix possible ss bug
        sed -E "s/(tcp|udp)/\\1 /g"
        
}

check_connections

exit 0