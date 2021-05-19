function readLanguageData(repo_url) {
    const repoURLComponents = repo_url.split("/");
    const repoName = repoURLComponents[repoURLComponents.length - 2];
    const url = `https://api.github.com/repos/cepdnaclk/${repoName}/languages`;

    $.ajax({
        type: "GET",
        url: url,
        dataType: "json",
        success: function(data) {
            var total = 0;
            var count = 0;
            var langList = {};
            $.each(data, function(lang, usage) {
                total += usage;
                count += 1;
                langList[lang] = usage;
            });

            if (count > 0) {
                $(".langData").removeClass("d-none");

                $.each(langList, function(lang, usage) {
                    var p = usage / total;
                    var val = Math.round(p * 10000) / 100;

                    if (val >= 0.25) {
                        $("#langList").append(`<li>${lang} - ${val}%</li>`);
                    }
                });
            }
        }
    });
}

function readRemoteData(page_url) {
    const url = `${page_url}/data/index.json`;

    $.ajax({
        type: "GET",
        url: url,
        dataType: "json",
        success: function(data) {
            let visibility = true; // data.visibility

            if (visibility == true) {
                // Show remoteData container
                $(".remoteData").removeClass("d-none");

                if (data.team[0].name != "Team Member Name 1") {
                    $(".remoteDataTeam").removeClass("d-none");
                    $.each(data.team, function(index, member) {
                        $("#teamList").append(
                            `<li>${member.eNumber}, ${member.name}, <a href="mailto:${member.email}">${member.email}</a></li>`
                            // TODO: Add other profile links
                        );
                    });
                }

                if (data.supervisors[0].name != "Dr. Supervisor 1") {
                    $(".remoteDataSupervisors").removeClass("d-none");
                    $.each(data.supervisors, function(index, s) {
                        $("#supervisorList").append(
                            `<li>${s.name}, <a href="mailto:${s.email}">${s.email}</a></li>`
                            // TODO: Add other profile links
                        );
                    });
                }

                if (data.tags.length > 0) {
                    $(".remoteDataTags").removeClass("d-none");
                    $.each(data.tags, function(index, tag) {
                        $("#tagList").append(`<span class='tag'>${tag}</span> `);
                    });
                }

                if (data.publications != null && data.publications.length > 0) {
                    let count = 0;

                    $.each(data.publications, function(index, pub) {
                        // "title":"Paper Title",
                        // "journal":"Journal or Conference Name",
                        // "description":"Sample Description",
                        // "url":"#"

                        if (
                            pub.title !== "Paper Title" &&
                            pub.journal !== "Journal or Conference Name" &&
                            pub.description !== "Sample Description"
                        ) {
                            $("#publicationsURL").append("<li><div>");
                            $("#publicationsURL").append(
                                "<a href='" +
                                pub.url +
                                "' target='_blank'>" +
                                pub.title +
                                "</a>, " +
                                pub.journal +
                                "<br>"
                            );
                            $("#publicationsURL").append(
                                "<small>" + pub.description + "</small>"
                            );
                            $("#publicationsURL").append("</div></li>");
                        }
                    });

                    if (count > 0) {
                        $("#publications").removeClass("d-none");
                    }
                }

                if (data.media != null && data.media.length > 0) {
                    let count = 0;

                    $.each(data.media, function(index, media) {
                        if (media.type === "youtube" && media.url.length > 0) {
                            if (!(media.title == "" || media.url =="#")) {
                                // Show the title
                                $("#youtubeVideoDiv").append("<h4>" + media.title + "</h4>");

                                $("#youtubeVideoDiv").append(
                                    "<div class='video-container'><iframe width='100%' src='" +
                                    media.url +
                                    "' frameborder='1' allow='accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture' allowfullscreen=''>"
                                );
                                $("#youtubeVideoDiv").append("</iframe></div>");
                                $("#youtubeVideoDiv").append("<br><br>");
                                count++;
                            }
                        } else {
                            // Only supported youtube videos for now
                        }
                    });

                    if (count > 0) {
                        $("#youtubeVideo").removeClass("d-none");
                    }
                }

                // Removed, since it is already provided
                // $("#descriptionText").html(`<p>${data.description}</p>`);
            }
        }
    });
}
