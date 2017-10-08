<xsl:transform version="1.0"
	       xmlns:xsl="http://www.w3.org/1999/XSL/Transform">
  <xsl:output omit-xml-declaration="yes" indent="yes"/>

  <xsl:template match="*">
    <xsl:copy>
      <xsl:copy-of select="@*"/>
      <xsl:apply-templates select="node()"/>
    </xsl:copy>
  </xsl:template>

  <xsl:template match="node()[self::p or
		       self::em or
		       self::a or
		       self::li]/text()" name="nobreaks">
    <xsl:param name="pText" select="."/>

    <xsl:choose>
      <xsl:when test="not(contains($pText, '&#xA;'))">
	<xsl:copy-of select="$pText"/>
      </xsl:when>
      <xsl:otherwise>
	<xsl:value-of select="substring-before($pText, '&#xA;')"/>
	<xsl:element name="span">
	  <xsl:attribute name="class">
	    <xsl:value-of select="'nobr'"/>
	  </xsl:attribute>
	  <xsl:value-of select="' '"/>
	</xsl:element>
	<xsl:call-template name="nobreaks">
          <xsl:with-param name="pText" select=
			  "substring-after($pText, '&#xA;')"/>
	</xsl:call-template>
      </xsl:otherwise>
    </xsl:choose>
  </xsl:template>
</xsl:transform>
