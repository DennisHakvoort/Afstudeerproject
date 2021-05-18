package nl.avisi.kitea.rest;

import com.atlassian.plugins.rest.common.security.AnonymousAllowed;

import javax.inject.Inject;
import javax.ws.rs.GET;
import javax.ws.rs.Path;
import javax.ws.rs.Produces;
import javax.ws.rs.QueryParam;
import javax.ws.rs.core.MediaType;
import javax.ws.rs.core.Response;
import java.time.Instant;
import java.time.format.DateTimeFormatter;
import java.time.temporal.TemporalAccessor;
import java.util.Date;

/**
 * A resource of message.
 */
@Path("/recent")
public class RecentPageApi {
    @Inject
    private final FetchPagesSince recentFetcher;

    public RecentPageApi(FetchPagesSince recentFetcher) {
        this.recentFetcher = recentFetcher;
    }

    @GET
    @AnonymousAllowed
    @Produces({MediaType.APPLICATION_JSON, MediaType.APPLICATION_JSON})
    public Response fetchPagesSinceDate(@QueryParam("date") String dateString) {
        // We're using the datestring as defined in ISO-8601, this code is from:
        // https://stackoverflow.com/questions/2201925/converting-iso-8601-compliant-string-to-java-util-date/60214805#60214805
        TemporalAccessor temporalAccessor = DateTimeFormatter.ISO_INSTANT.parse(dateString);
        Instant instant = Instant.from(temporalAccessor);
        Date date = Date.from(instant);
        return Response.ok(recentFetcher.fetchPagesSinceDate(date)).build();

    }
}