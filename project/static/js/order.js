function loadSummary() {
                var complexOrders = ["Physics", "Engineering", "SPSS", "Mathematics", "Chemistry", "Statistics", "Architecture", "Civil Engineering", "AutoCAD", "MatLAB", "Programming", "Software Based"];
                var price_per_page = 0;
                var ac_level = document.getElementById("ac_level").value;
                document.getElementById("ac_level_summary").innerHTML = '<i class="fas fa-user-graduate"></i> ' + ac_level;
                var discipline = document.getElementById("discipline").value;
                document.getElementById("discipline_summary").innerHTML = '<i class="fas fa-graduation-cap"></i> ' + discipline;
                var deadline = document.getElementById("due_date").value;

                var p_type = document.getElementById("paper_type").value;
                document.getElementById("p_type_summary").innerHTML = '<i class="fas fa-pen-alt"></i> ' + p_type;

                var total_price = 0;

                if (complexOrders.includes(discipline)) {
                  switch (parseFloat(deadline)) {
                      case 336:
                          switch (ac_level) {
                            case "High School":
                              price_per_page = parseFloat(17.50);
                              break;
                            case "College":
                              price_per_page = parseFloat(19.50);
                              break;
                            case "Undergraduate":
                              price_per_page = parseFloat(21.50);
                              break;
                            case "Master":
                              price_per_page = parseFloat(23.50);
                              break;
                            case "PhD":
                              price_per_page = parseFloat(25.50);
                          }
                          break;
                        case 288:
                          switch (ac_level) {
                            case "High School":
                              price_per_page = parseFloat(20.40);
                              break;
                            case "College":
                              price_per_page = parseFloat(22.40);
                              break;
                            case "Undergraduate":
                              price_per_page = parseFloat(24.40);
                              break;
                            case "Master":
                              price_per_page = parseFloat(26.40);
                              break;
                            case "PhD":
                              price_per_page = parseFloat(28.40);
                          }
                          break;
                        case 240:
                          switch (ac_level) {
                            case "High School":
                              price_per_page = parseFloat(23.30);
                              break;
                            case "College":
                              price_per_page = parseFloat(25.30);
                              break;
                            case "Undergraduate":
                              price_per_page = parseFloat(27.30);
                              break;
                            case "Master":
                              price_per_page = parseFloat(29.30);
                              break;
                            case "PhD":
                              price_per_page = parseFloat(31.30);
                          }
                          break;
                        case 216:
                          switch (ac_level) {
                            case "High School":
                              price_per_page = parseFloat(26.20);
                              break;
                            case "College":
                              price_per_page = parseFloat(28.20);
                              break;
                            case "Undergraduate":
                              price_per_page = parseFloat(30.20);
                              break;
                            case "Master":
                              price_per_page = parseFloat(32.20);
                              break;
                            case "PhD":
                              price_per_page = parseFloat(34.20);
                          }
                          break;
                        case 192:
                          switch (ac_level) {
                            case "High School":
                              price_per_page = parseFloat(29.10);
                              break;
                            case "College":
                              price_per_page = parseFloat(31.10);
                              break;
                            case "Undergraduate":
                              price_per_page = parseFloat(33.10);
                              break;
                            case "Master":
                              price_per_page = parseFloat(35.10);
                              break;
                            case "PhD":
                              price_per_page = parseFloat(37.10);
                          }
                          break;
                        case 168:
                          switch (ac_level) {
                            case "High School":
                              price_per_page = parseFloat(32.00);
                              break;
                            case "College":
                              price_per_page = parseFloat(34.00);
                              break;
                            case "Undergraduate":
                              price_per_page = parseFloat(36.00);
                              break;
                            case "Master":
                              price_per_page = parseFloat(38.00);
                              break;
                            case "PhD":
                              price_per_page = parseFloat(40.00);
                          }
                          break;
                        case 144:
                          switch (ac_level) {
                            case "High School":
                              price_per_page = parseFloat(34.90);
                              break;
                            case "College":
                              price_per_page = parseFloat(36.90);
                              break;
                            case "Undergraduate":
                              price_per_page = parseFloat(38.90);
                              break;
                            case "Master":
                              price_per_page = parseFloat(40.90);
                              break;
                            case "PhD":
                              price_per_page = parseFloat(42.90);
                          }
                          break;
                        case 120:
                          switch (ac_level) {
                            case "High School":
                              price_per_page = parseFloat(37.80);
                              break;
                            case "College":
                              price_per_page = parseFloat(39.80);
                              break;
                            case "Undergraduate":
                              price_per_page = parseFloat(41.80);
                              break;
                            case "Master":
                              price_per_page = parseFloat(43.80);
                              break;
                            case "PhD":
                              price_per_page = parseFloat(45.80);
                          }
                          break;
                        case 96:
                          switch (ac_level) {
                            case "High School":
                              price_per_page = parseFloat(40.40);
                              break;
                            case "College":
                              price_per_page = parseFloat(42.40);
                              break;
                            case "Undergraduate":
                              price_per_page = parseFloat(44.40);
                              break;
                            case "Master":
                              price_per_page = parseFloat(46.40);
                              break;
                            case "PhD":
                              price_per_page = parseFloat(48.40);
                          }
                          break;
                        case 72:
                          switch (ac_level) {
                            case "High School":
                              price_per_page = parseFloat(43.00);
                              break;
                            case "College":
                              price_per_page = parseFloat(45.00);
                              break;
                            case "Undergraduate":
                              price_per_page = parseFloat(47.00);
                              break;
                            case "Master":
                              price_per_page = parseFloat(49.00);
                              break;
                            case "PhD":
                              price_per_page = parseFloat(51.00);
                          }
                          break;
                        case 48:
                          switch (ac_level) {
                            case "High School":
                              price_per_page = parseFloat(45.60);
                              break;
                            case "College":
                              price_per_page = parseFloat(47.60);
                              break;
                            case "Undergraduate":
                              price_per_page = parseFloat(49.60);
                              break;
                            case "Master":
                              price_per_page = parseFloat(51.60);
                              break;
                            case "PhD":
                              price_per_page = parseFloat(53.60);
                          }
                          break;
                        case 24:
                          switch (ac_level) {
                            case "High School":
                              price_per_page = parseFloat(48.20);
                              break;
                            case "College":
                              price_per_page = parseFloat(50.20);
                              break;
                            case "Undergraduate":
                              price_per_page = parseFloat(52.20);
                              break;
                            case "Master":
                              price_per_page = parseFloat(54.20);
                              break;
                            case "PhD":
                              price_per_page = parseFloat(56.20);
                          }
                          break;
                        case 12:
                          switch (ac_level) {
                            case "High School":
                              price_per_page = parseFloat(50.80);
                              break;
                            case "College":
                              price_per_page = parseFloat(52.80);
                              break;
                            case "Undergraduate":
                              price_per_page = parseFloat(54.80);
                              break;
                            case "Master":
                              price_per_page = parseFloat(56.80);
                              break;
                            case "PhD":
                              price_per_page = parseFloat(58.80);
                          }
                          break;
                        case 8:
                          switch (ac_level) {
                            case "High School":
                              price_per_page = parseFloat(53.40);
                              break;
                            case "College":
                              price_per_page = parseFloat(55.40);
                              break;
                            case "Undergraduate":
                              price_per_page = parseFloat(57.40);
                              break;
                            case "Master":
                              price_per_page = parseFloat(59.40);
                              break;
                            case "PhD":
                              price_per_page = parseFloat(61.40);
                          }
                          break;
                        case 4:
                          switch (ac_level) {
                            case "High School":
                              price_per_page = parseFloat(56.60);
                              break;
                            case "College":
                              price_per_page = parseFloat(58.60);
                              break;
                            case "Undergraduate":
                              price_per_page = parseFloat(60.60);
                              break;
                            case "Master":
                              price_per_page = parseFloat(62.60);
                              break;
                            case "PhD":
                              price_per_page = parseFloat(64.60);
                          }
                          break;
                        default:
                          alert("ERROR!");
                    }
                } else {
                    switch (parseFloat(deadline)) {
                      case 336:
                          switch (ac_level) {
                            case "High School":
                              price_per_page = parseFloat(12.40);
                              break;
                            case "College":
                              price_per_page = parseFloat(13.90);
                              break;
                            case "Undergraduate":
                              price_per_page = parseFloat(15.40);
                              break;
                            case "Master":
                              price_per_page = parseFloat(16.90);
                              break;
                            case "PhD":
                              price_per_page = parseFloat(18.40);
                          }
                          break;
                        case 288:
                          switch (ac_level) {
                            case "High School":
                              price_per_page = parseFloat(15.30);
                              break;
                            case "College":
                              price_per_page = parseFloat(16.80);
                              break;
                            case "Undergraduate":
                              price_per_page = parseFloat(18.30);
                              break;
                            case "Master":
                              price_per_page = parseFloat(19.80);
                              break;
                            case "PhD":
                              price_per_page = parseFloat(21.30);
                          }
                          break;
                        case 240:
                          switch (ac_level) {
                            case "High School":
                              price_per_page = parseFloat(18.20);
                              break;
                            case "College":
                              price_per_page = parseFloat(19.70);
                              break;
                            case "Undergraduate":
                              price_per_page = parseFloat(21.20);
                              break;
                            case "Master":
                              price_per_page = parseFloat(22.70);
                              break;
                            case "PhD":
                              price_per_page = parseFloat(24.20);
                          }
                          break;
                        case 216:
                          switch (ac_level) {
                            case "High School":
                              price_per_page = parseFloat(21.10);
                              break;
                            case "College":
                              price_per_page = parseFloat(22.60);
                              break;
                            case "Undergraduate":
                              price_per_page = parseFloat(24.10);
                              break;
                            case "Master":
                              price_per_page = parseFloat(25.60);
                              break;
                            case "PhD":
                              price_per_page = parseFloat(27.10);
                          }
                          break;
                        case 192:
                          switch (ac_level) {
                            case "High School":
                              price_per_page = parseFloat(24.00);
                              break;
                            case "College":
                              price_per_page = parseFloat(25.50);
                              break;
                            case "Undergraduate":
                              price_per_page = parseFloat(27.00);
                              break;
                            case "Master":
                              price_per_page = parseFloat(28.50);
                              break;
                            case "PhD":
                              price_per_page = parseFloat(30.00);
                          }
                          break;
                        case 168:
                          switch (ac_level) {
                            case "High School":
                              price_per_page = parseFloat(26.90);
                              break;
                            case "College":
                              price_per_page = parseFloat(28.40);
                              break;
                            case "Undergraduate":
                              price_per_page = parseFloat(29.90);
                              break;
                            case "Master":
                              price_per_page = parseFloat(31.40);
                              break;
                            case "PhD":
                              price_per_page = parseFloat(32.90);
                          }
                          break;
                        case 144:
                          switch (ac_level) {
                            case "High School":
                              price_per_page = parseFloat(29.80);
                              break;
                            case "College":
                              price_per_page = parseFloat(31.30);
                              break;
                            case "Undergraduate":
                              price_per_page = parseFloat(32.80);
                              break;
                            case "Master":
                              price_per_page = parseFloat(34.30);
                              break;
                            case "PhD":
                              price_per_page = parseFloat(35.80);
                          }
                          break;
                        case 120:
                          switch (ac_level) {
                            case "High School":
                              price_per_page = parseFloat(32.70);
                              break;
                            case "College":
                              price_per_page = parseFloat(34.20);
                              break;
                            case "Undergraduate":
                              price_per_page = parseFloat(35.70);
                              break;
                            case "Master":
                              price_per_page = parseFloat(37.20);
                              break;
                            case "PhD":
                              price_per_page = parseFloat(38.70);
                          }
                          break;
                        case 96:
                          switch (ac_level) {
                            case "High School":
                              price_per_page = parseFloat(35.30);
                              break;
                            case "College":
                              price_per_page = parseFloat(37.10);
                              break;
                            case "Undergraduate":
                              price_per_page = parseFloat(38.30);
                              break;
                            case "Master":
                              price_per_page = parseFloat(39.80);
                              break;
                            case "PhD":
                              price_per_page = parseFloat(42.60);
                          }
                          break;
                        case 72:
                          switch (ac_level) {
                            case "High School":
                              price_per_page = parseFloat(37.90);
                              break;
                            case "College":
                              price_per_page = parseFloat(39.60);
                              break;
                            case "Undergraduate":
                              price_per_page = parseFloat(40.90);
                              break;
                            case "Master":
                              price_per_page = parseFloat(42.40);
                              break;
                            case "PhD":
                              price_per_page = parseFloat(45.20);
                          }
                          break;
                        case 48:
                          switch (ac_level) {
                            case "High School":
                              price_per_page = parseFloat(40.50);
                              break;
                            case "College":
                              price_per_page = parseFloat(42.10);
                              break;
                            case "Undergraduate":
                              price_per_page = parseFloat(43.50);
                              break;
                            case "Master":
                              price_per_page = parseFloat(45.00);
                              break;
                            case "PhD":
                              price_per_page = parseFloat(47.80);
                          }
                          break;
                        case 24:
                          switch (ac_level) {
                            case "High School":
                              price_per_page = parseFloat(43.10);
                              break;
                            case "College":
                              price_per_page = parseFloat(44.60);
                              break;
                            case "Undergraduate":
                              price_per_page = parseFloat(46.10);
                              break;
                            case "Master":
                              price_per_page = parseFloat(47.60);
                              break;
                            case "PhD":
                              price_per_page = parseFloat(50.40);
                          }
                          break;
                        case 12:
                          switch (ac_level) {
                            case "High School":
                              price_per_page = parseFloat(45.70);
                              break;
                            case "College":
                              price_per_page = parseFloat(47.20);
                              break;
                            case "Undergraduate":
                              price_per_page = parseFloat(48.70);
                              break;
                            case "Master":
                              price_per_page = parseFloat(50.20);
                              break;
                            case "PhD":
                              price_per_page = parseFloat(53.00);
                          }
                          break;
                        case 8:
                          switch (ac_level) {
                            case "High School":
                              price_per_page = parseFloat(48.30);
                              break;
                            case "College":
                              price_per_page = parseFloat(50.10);
                              break;
                            case "Undergraduate":
                              price_per_page = parseFloat(51.60);
                              break;
                            case "Master":
                              price_per_page = parseFloat(53.10);
                              break;
                            case "PhD":
                              price_per_page = parseFloat(57.50);
                          }
                          break;
                        case 4:
                          switch (ac_level) {
                            case "High School":
                              price_per_page = parseFloat(50.60);
                              break;
                            case "College":
                              price_per_page = parseFloat(54.50);
                              break;
                            case "Undergraduate":
                              price_per_page = parseFloat(56.00);
                              break;
                            case "Master":
                              price_per_page = parseFloat(59.50);
                              break;
                            case "PhD":
                              price_per_page = parseFloat(62.80);
                          }
                          break;
                        default:
                          alert("ERROR!");
                    } 
                    //alert(price_per_page);
                }
                

                var pages = document.getElementById("t_pages").value;
                var opt_1 = document.getElementById("opt_1");
                if (opt_1.checked) {
                    document.getElementById("w_count").value = "(500 words)";
                    price_per_page = price_per_page * 2;
                } else {
                    price_per_page = price_per_page * 1;
                }
                total_price = pages * price_per_page;
                if (pages == 1) {
                  document.getElementById("pages_summary").value = pages + " page x $" + price_per_page.toFixed(2);
                } else {
                  document.getElementById("pages_summary").value = pages + " pages x $" + price_per_page.toFixed(2);
                }
                
                document.getElementById("pages_summary").style.fontSize = "13px";
                document.getElementById("summary_total").value = "$" + total_price.toFixed(2) + " USD";
                document.getElementById("summary_total").style.fontSize = "13px";
                document.getElementById("grand_total").innerHTML = "$" + total_price.toFixed(2) + " USD";
                document.getElementById("g_total").value = total_price.toFixed(2);
            }