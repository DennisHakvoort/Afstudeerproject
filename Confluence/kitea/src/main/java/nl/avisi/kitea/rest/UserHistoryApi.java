package nl.avisi.kitea.rest;

import com.atlassian.plugins.rest.common.security.AnonymousAllowed;
import nl.avisi.kitea.model.UserHistory;
import nl.avisi.kitea.model.UserKey;

import javax.inject.Inject;
import javax.inject.Named;
import javax.ws.rs.*;
import javax.ws.rs.core.MediaType;
import javax.ws.rs.core.Response;
import javax.xml.bind.annotation.XmlElement;
import java.time.Instant;
import java.time.LocalDateTime;
import java.util.Date;
import java.util.Locale;
import java.util.TimeZone;

/**
 * A resource of message.
 */
@Named
@Path("/history")
public class UserHistoryApi {
    @Inject
    private final FetchUserHistory userhistoryFetcher;

    public UserHistoryApi(FetchUserHistory userhistoryFetcher) {
        this.userhistoryFetcher = userhistoryFetcher;
    }

    @GET
    @Produces({MediaType.APPLICATION_JSON, MediaType.APPLICATION_JSON})
    public Response fetchUserHistory(@XmlElement UserKey userKey) {
        Response response = null;
        String key = userKey.getUserKey();
        System.out.println(userKey.getUserKey());
        if (key != null) {
            response = Response.ok(this.userhistoryFetcher.fetch(userKey.getUserKey())).build();
            System.out.println(response.getStatus());
            System.out.println(response.getEntity());
            return response;
        } else {
            return Response.ok(new UserHistory("please", "add a username")).build();
        }
    }
}