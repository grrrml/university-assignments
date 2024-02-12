using Plots
using Random

# Testy dotyczące szerokości drzwi, ilości ludzi były wykonywane przez zmianę funkcji create_layout i add_people
# Testy dotyczące ilości zajętych pomieszczeń zostały wykonane przez komentowanie poszczególnych fragmentów funkcji add_people

#=
Wersja 2: Ludzie nie ustawiają się w "kolejce po skosie",
szukają innej optymalnej drogi idąc na pola o równej wartości

Odległość mierzona w metryce Czebyszewa

Oznaczenia:
W szablonie: 0 = puste pole ; 1 = ściana ; 2 = wyjście ; 3 = osoba
W warstwie liczacej odległość(cell_values_layer): -1 = ściana ; >=1 = odległość od wyjścia
=#

function create_layout()  #tworzy szablon pomieszczenia, n - wymiar kwadratowej planszy
    n = 65
    layer = zeros(n, n)
    layer[1,:] .= 1
    layer[n,:] .= 1
    layer[:,1] .= 1
    layer[:,n] .= 1

    layer[n, n ÷ 2:n ÷ 2] .= 2 #wyjście

    layer[1:9 , 38] .= 1
    layer[14:31 , 38] .= 1
    layer[36:53 , 38] .= 1
    layer[58:64 , 38] .= 1
    layer[1:9 , 26] .= 1
    layer[14:31 , 26] .= 1
    layer[36:53, 26] .= 1
    layer[58:64, 26] .= 1
    layer[n ÷ 3 + 1, 38:n] .= 1
    layer[2n ÷ 3 + 1, 38:n] .= 1
    layer[n ÷ 3 + 1, 1:26] .= 1
    layer[2n ÷ 3 + 1, 1:26] .= 1
    return layer
end

function cell_values_layer(map_layout) #tworzy warstwę z wartościami pól (odległościami od wyjścia), n - wymiar planszy
    n = 65
    value_map = copy(map_layout)
    value_map[value_map .== 1] .= -1 #zamieniam żeby uniknąć kolizji oznaczeń
    value_map[value_map .== 2] .= 1  #wyjście ma odległość 1
    prev_value = 1

    while 0 in value_map #dopóki są komórki bez obliczonej odległości
        current_value = prev_value + 1 
        for i in 2:n-1, j in 2:n-1
            if prev_value in value_map[i-1:i+1, j-1:j+1] && value_map[i, j] == 0
                value_map[i, j] = current_value
            end
        end
        prev_value += 1
    end
    return value_map
end

function add_people(map_layout) # dodaje ludzi na planszę, P - ilość ludzi, map_layout - szablon planszy
    people_place = []
    lend = 16 #  zmiana 20->140, 18->120, 16->100, 14->80, 12->60 osób
    rend = 50 # 46->140, 48->120, 50->100, 52->80, 54->60
    for i in 6:16, j in 6:lend#dół lewa
        map_layout[i, j] = 3
        push!(people_place, (i, j))
    end
    for i in 25:35, j in 6:lend #środek lewa
        map_layout[i, j] = 3
        push!(people_place, (i, j))
    end
    for i in 50:60, j in 6:lend#góra lewa
        map_layout[i, j] = 3
        push!(people_place, (i, j))
    end
    for i in 6:16, j in rend:60#dół prawa
        map_layout[i, j] = 3
        push!(people_place, (i, j))
    end
    for i in 25:35, j in rend:60#środek prawa
        map_layout[i, j] = 3
        push!(people_place, (i, j))
    end
    for i in 50:60, j in rend:60#góra prawa
        map_layout[i, j] = 3
        push!(people_place, (i, j))
    end
    return (map_layout, people_place)
end

function choose(array) #wybiera losowy element z listy
    len = length(array)
    id = rand(1:len)
    return array[id]
end

function move(map_layout, value_map, people_place) #obsługuje ruch ludzi, people_place - lista pozycji wszytskich ludzi
    for p in 1:length(people_place) # p to numer komórki w liście ludzi
        if people_place[p] == false #jeśli dany agent juz wyszedł przejdź do kolejnego
            continue
        end
        x = people_place[p][1] #współrzędna x p-tego agenta
        y = people_place[p][2] #współrzędna y p-tego agenta
        av_cells = [] #komórki, do których można się przenieść
        av_equal_cells = [] #komórki, do których można się przenieść o tej samej odległości
        for i in x-1:x+1, j in y-1:y+1
            if (map_layout[i, j] == 0 || map_layout[i, j] == 2) && value_map[i, j] == value_map[x, y] - 1 #pole jest puste/wyjściem
                push!(av_cells, (i, j))
            elseif (map_layout[i, j] == 0 || map_layout[i, j] == 2) && value_map[i, j] == value_map[x, y] #pole jest puste/wyjściem
                push!(av_equal_cells, (i, j))
            end
        end

        if length(av_cells) != 0 #jeśli są dostępne komórki
            old_coords = people_place[p] #stare współrzędne agenta
            new_coords = choose(av_cells) #nowe współrzędne agenta
            people_place[p] = new_coords #zmiana współrzędnych agenta
            if value_map[people_place[p][1], people_place[p][2]] == 1 #jeśli agent jest w drzwiach
                map_layout[old_coords[1], old_coords[2]] = 0 #wychodzi, więc pole zostaje puste
                people_place[p] = false
            else
                (map_layout[old_coords[1], old_coords[2]], map_layout[new_coords[1], new_coords[2]]) = 
                (map_layout[new_coords[1], new_coords[2]], map_layout[old_coords[1], old_coords[2]]) #zamieniam pola na planszy
            end
        else 
            if length(av_equal_cells) != 0 #jeśli są dostępne komórki równe, ale nie ma lepszych (reszta tak jak powyżej)
                old_coords = people_place[p] 
                new_coords = choose(av_equal_cells) 
                people_place[p] = new_coords 
                if value_map[people_place[p][1], people_place[p][2]] == 1 
                    map_layout[old_coords[1], old_coords[2]] = 0
                    people_place[p] = false
                else
                    (map_layout[old_coords[1], old_coords[2]], map_layout[new_coords[1], new_coords[2]]) = 
                    (map_layout[new_coords[1], new_coords[2]], map_layout[old_coords[1], old_coords[2]]) #zamieniam pola na planszy
                end
            end
        end

    end
end

function evacuation(map_layout, value_map, people_place) #gif ewakuacji, wypisuje czas ewakuacji
    an = Animation()
    t = 0
    while 3 in map_layout
        t += 1
        map = heatmap(map_layout,
        aspect_ratio = 1,
        seriescolor = palette([:white, :black, :lime, :blue]),
        colorbar = false,
        xlims = (0, size(map_layout, 1)),
        ylims = (0, size(map_layout, 2))
        )
        frame(an, map)
        move(map_layout, value_map, people_place)
    end
    println(t)
    return gif(an, fps=5)
end

function draw_layout(matrix) #(rysunek) szablon planszy z ludźmi
    heatmap(matrix,
        aspect_ratio = 1,
        seriescolor = palette([:white, :black, :lime, :blue]),
        colorbar = false,
        xlims = (0, size(matrix, 1)),
        ylims = (0, size(matrix, 2))
        )  
end

function draw_value_map(matrix) #(rysunek) pokazuje odległość każdego pola od wyjścia
    heatmap(matrix,
        aspect_ratio = 1,
        seriescolor = cgrad([:yellow,:darkred]),
        xlims = (0, size(matrix, 1)),
        ylims = (0, size(matrix, 2)),
        title = "Odległość od wyjścia"    
        ) 
end

map_layout = create_layout() #kształt planszy
value_map = cell_values_layer(map_layout) #plansza z wartościami pól
(map_layout, people_place) = add_people(map_layout) #plansza z ludźmi, położenie ludzi w wektorze
evacuation(map_layout, value_map, people_place)