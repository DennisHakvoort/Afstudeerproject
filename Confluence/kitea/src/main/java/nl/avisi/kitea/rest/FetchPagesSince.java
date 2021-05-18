package nl.avisi.kitea.rest;

import com.atlassian.confluence.pages.Page;
import com.atlassian.confluence.pages.PageManager;
import com.atlassian.plugin.spring.scanner.annotation.imports.ConfluenceImport;
import nl.avisi.kitea.model.PageDTO;

import javax.inject.Inject;
import java.util.*;
import javax.inject.Named;

@Named
public class FetchPagesSince {
    @ConfluenceImport
    private final PageManager pageManager;

    @Inject
    public FetchPagesSince(PageManager pageManager) {
        this.pageManager = pageManager;
    }

    public PageDTO[] fetchPagesSinceDate(Date date) {
        List<Page> newPages = this.pageManager.getPagesCreatedOrUpdatedSinceDate(date);
        PageDTO[] fetchedPages = new PageDTO[newPages.size()];
        for (int i = 0; i < newPages.size(); i++) {
            Page currentPage = newPages.get(i);
            fetchedPages[i] = new PageDTO(
                    currentPage.getIdAsString(),
                    currentPage.getBodyAsStringWithoutMarkup(),
                    currentPage.getTitle(),
                    currentPage.getSpace().getName()
            );
        }
        return fetchedPages;
    }
}
